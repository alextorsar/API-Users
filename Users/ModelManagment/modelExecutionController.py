from ..models import Models
import pysd
from APIUsers import settings
import os.path
import math

class NotAllowedAccess(Exception):
    message = "You are not allowed to access this model"

class IncorrectModelPath(Exception):
    message = "The model path was not correct"

class IncorrectFileExtension(Exception):
    message = "Only .xmile files are allowed"

class IncorrectModelDefinition(Exception):
    message = "The model was not correctly defined"

def getModelFromPath(modelPath):
    try:
        file, extension = os.path.splitext(modelPath)
        path = file + ".py"
        return pysd.load(path)
    except Exception:
        raise IncorrectModelPath()

def loadModel(modelPath):
    file, extension = os.path.splitext(modelPath)
    try:
        if extension == '.xmile':
            pysd.read_xmile(modelPath)
        elif extension == '.mdl':
            pysd.read_vensim(modelPath)
        else:
            raise IncorrectFileExtension()
    except Exception:
        raise IncorrectModelDefinition()

def splitLimitsAttributes(variables):
    i = 0
    for variable in variables:
        variable['key'] = i
        i = i + 1
        (upperLimit,lowerLimit) = variable['Limits']
        if(math.isnan(upperLimit)):
            variable['UpperLimit'] = None
        else:
            variable['UpperLimit'] = upperLimit
        if(math.isnan(lowerLimit)):
            variable['LowerLimit'] = None
        else:
            variable['LowerLimit'] = lowerLimit
        del variable['Limits']
    return variables

def getModelDocumentation(modelId,userId):
    model = Models.objects.filter(id_user=userId, id=modelId).first()
    if model is not None:
        model = getModelFromPath(os.path.join(settings.MEDIA_ROOT,str(model.file)))
        result = model.doc.to_dict(orient="records")
        result = splitLimitsAttributes(result)
        return result
    else:
        raise NotAllowedAccess()
    
def getModelExecutionResult(modelId,userId):
    model = Models.objects.filter(id_user=userId, id=modelId).first()
    if model is not None:
        model = getModelFromPath(os.path.join(settings.MEDIA_ROOT,str(model.file)))
        result = model.run()
        return result
    else:
        raise NotAllowedAccess()