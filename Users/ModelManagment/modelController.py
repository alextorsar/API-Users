from ..serializers import ModelSerializer
from ..SubModelManagment import subModelController
from .modelExecutionController import loadModel
from ..models import Models
import os
from APIUsers import settings
from shutil import rmtree
from ..exceptions import ModelExceptions

def createModel(request):
    serializer = saveModelToDatabase(modelData=request.data)
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