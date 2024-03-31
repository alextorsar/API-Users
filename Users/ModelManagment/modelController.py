from ..serializers import ModelSerializer
from ..SubModelManagment import subModelController
from .modelExecutionController import loadModel
from ..models import Models, SubModels
import os
from APIUsers import settings
from shutil import rmtree, move
from ..exceptions import ModelExceptions
import lxml.etree

def createModel(request):
    serializer = saveModelToDatabase(modelData=request.data)
    if not containsDefaultSimSpecs(serializer.data['id']):
        addDefaultSimSpecs(serializer.data['id'])
    if request.data.get('submodels'):
        submodels = request.data.getlist('submodels')
        for submodel in submodels:
            subModelObject = {
                'id_model':serializer.data['id'],
                'file':submodel
            }
            try:
                subModelController.createSubmodel(subModelObject)
            except Exception as e:
                deleteModel(serializer.data['id'],serializer.data['id_user'])
                raise e
    try:
        transformModel(serializer.data['id'])
    except Exception as e:
        deleteModel(serializer.data['id'],serializer.data['id_user'])
        raise e
    return serializer.data

def deleteModel(modelId,userId):
    model = Models.objects.filter(id_user=userId, id=modelId).first()
    if (model is not None):
        serializer = ModelSerializer(model)
        rmtree(os.path.join(settings.MEDIA_ROOT, "models", str(serializer.data['id_user']), serializer.data['name']))
        model.delete()
    else:
        raise ModelExceptions.NotAllowedAccess()

def updateModel(newModel,userId):
    model = Models.objects.filter(id_user=userId, id=newModel['id']).first()
    oldImage = oldFile = oldName = None
    newSubModels = []
    if(model is not None):
        if 'name' in newModel and model.name != newModel['name']:
            fileSrc = str(model.file)
            imageSrc = str(model.image)
            model.file = os.path.join(settings.MEDIA_ROOT, "models", str(userId), newModel['name'], "files", fileSrc.split("/")[-1])
            model.image = os.path.join(settings.MEDIA_ROOT, "models", str(userId), newModel['name'], "image", imageSrc.split("/")[-1])
            oldName = model.name
            url = os.path.join(settings.MEDIA_ROOT, "models", str(userId))
            os.rename(os.path.join(url,model.name),os.path.join(url,newModel['name']))
            model.name=newModel['name']
        if 'image' in newModel:
            oldImage = model.image
            model.image=newModel['image']
        if 'file' in newModel:
            oldFile = model.file
            model.file=newModel['file']
        if 'subModelsToDelete' in newModel:
            auxDirectory = os.path.join(settings.MEDIA_ROOT, newModel['id'])
            os.mkdir(auxDirectory)
            subModelsToDelete = newModel.getlist('subModelsToDelete')
            for subModelId in subModelsToDelete: 
                subModel = SubModels.objects.filter(id=subModelId).first()
                try:
                    move(os.path.join(settings.MEDIA_ROOT,str(subModel.file)), auxDirectory)
                except Exception as e:    
                    raise e
        if 'submodels' in newModel:
            submodels = newModel.getlist('submodels')
            for submodel in submodels:
                try:
                    subModelObject = {
                        'id_model':newModel['id'],
                        'file':submodel
                    }
                    newSubModels.append(subModelController.createSubmodel(subModelObject)['id'])
                except Exception as e:
                    raise e
        try:
            model.save()
            transformModel(newModel['id'])
            if 'image' in newModel:
                os.remove(os.path.join(settings.MEDIA_ROOT,str(oldImage)))
            if 'file' in newModel:
                os.remove(os.path.splitext(os.path.join(settings.MEDIA_ROOT,str(oldFile)))[0] + ".py")
                os.remove(os.path.join(settings.MEDIA_ROOT,str(oldFile)))
            if 'subModelsToDelete' in newModel:
                rmtree(os.path.join(settings.MEDIA_ROOT, newModel['id']))
                for subModelId in newModel.getlist('subModelsToDelete'):
                    subModelController.deleteSubModel(subModelId, userId)
            serializer = ModelSerializer(model)
            return serializer.data
        except Exception as e:
            if 'image' in newModel:
                os.remove(os.path.join(settings.MEDIA_ROOT,str(model.image)))
                model.image = oldImage
            if 'file' in newModel:
                os.remove(os.path.join(settings.MEDIA_ROOT,str(model.file)))
                model.file = oldFile
            if 'name' in newModel and oldName is not None:
                os.rename(os.path.join(url,model.name),os.path.join(url,oldName))
                model.name = oldName
            if 'subModelsToDelete' in newModel:
                for subModelId in newModel.getlist('subModelsToDelete'):
                    subModel = SubModels.objects.filter(id=subModelId).first()
                    move(os.path.join(settings.MEDIA_ROOT, newModel['id'], str(subModel.file).split("/")[-1]), os.path.join(settings.MEDIA_ROOT, str(subModel.file)))
                rmtree(os.path.join(settings.MEDIA_ROOT, newModel['id']))
            if 'submodels' in newModel:
                for subModelId in newSubModels:
                    subModel = SubModels.objects.filter(id=subModelId).first()
                    subModelController.deleteSubModel(subModelId, userId)
                    os.remove(os.path.join(settings.MEDIA_ROOT, str(subModel.file)))
            model.save()
            raise e
    else:
        raise ModelExceptions.NotAllowedAccess()

def getUserModels(userId):
    models = Models.objects.filter(id_user=userId)
    result = []
    for model in models:
        serializer = ModelSerializer(model)
        result.append(serializer.data)
    return result

def getModel(userId, modelId):
    model = Models.objects.filter(id_user=userId, id=modelId).first()
    if(model is not None):
        serializer = ModelSerializer(model)
        return serializer.data
    else:
        return None

        
def transformModel(modelId):
    try:
        model = Models.objects.filter(pk=modelId).first()
        loadModel(os.path.join(settings.MEDIA_ROOT,str(model.file)))
    except Exception as e:
        raise e
    
        
def saveModelToDatabase(modelData):
    serializer = ModelSerializer(data=modelData)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer

def containsDefaultSimSpecs(modelId):
    model = Models.objects.filter(pk=modelId).first()
    path = os.path.join(settings.MEDIA_ROOT,str(model.file))
    tree = lxml.etree.parse(path)
    expr = "//*[local-name() = $name]"
    r = tree.xpath(expr, name = "sim_specs")
    return len(r) > 0

def addDefaultSimSpecs(modelId):
    model = Models.objects.filter(pk=modelId).first()
    path = os.path.join(settings.MEDIA_ROOT,str(model.file))
    tree = lxml.etree.parse(path)
    root = tree.getroot()
    root.append(lxml.etree.XML("<sim_specs> <stop>30.0</stop><start>0.0</start><dt>0.125</dt></sim_specs>"))
    tree.write(path, pretty_print=True)