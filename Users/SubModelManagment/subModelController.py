from ..serializers import SubModelSerializer
from ..models import Models, SubModels
from ..exceptions import ModelExceptions
from ..ModelManagment import modelController

def createSubmodel(subModelData):
    serializer = SubModelSerializer(data=subModelData)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

def getSubModelsFromModel(idUser, parentId):
    parentModel = Models.objects.filter(id_user=idUser, id=parentId).first()
    if(parentModel is not None):
        submodels = SubModels.objects.filter(id_model=parentId)
        result = []
        for submodel in submodels:
            serializer = SubModelSerializer(submodel)
            result.append(serializer.data)
        return result
    else:
        return None

def getSubModelFromId(subModelId, parentId):
    submodel = SubModels.objects.filter(id=subModelId, id_model=parentId).first()
    if(submodel is not None):
        serializer = SubModelSerializer(submodel)
        return serializer.data
    else:
        raise 
    
def deleteSubModel(subModelId, userId):
    submodel = SubModels.objects.filter(id=subModelId).first()
    parentModel = Models.objects.filter(id_user=userId, id=submodel.id_model.id).first()   
    if (parentModel is not None):
        try:
            submodel.delete()
        except Exception as e:
            raise e
    else:
        raise ModelExceptions.NotAllowedAccess