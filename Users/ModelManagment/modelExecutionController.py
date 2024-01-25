from ..models import Models
import pysd
from APIUsers import settings
import os.path
import math
from ..exceptions import ModelExceptions,ModelExecutionExceptions

def getModelFromPath(modelPath):
    try:
        file, extension = os.path.splitext(modelPath)
        path = file + ".py"
        return pysd.load(path)
    except Exception:
        raise ModelExecutionExceptions.IncorrectModelPath()

def loadModel(modelPath):
    file, extension = os.path.splitext(modelPath)
    try:
        if extension == '.xmile':
            pysd.read_xmile(modelPath)
        else:
            raise ModelExecutionExceptions.IncorrectFileExtension()
    except Exception:
        raise ModelExecutionExceptions.IncorrectModelDefinition()

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
        raise ModelExceptions.NotAllowedAccess()
    
def getModelExecutionResult(modelId,userId):
    model = Models.objects.filter(id_user=userId, id=modelId).first()
    if model is not None:
        model = getModelFromPath(os.path.join(settings.MEDIA_ROOT,str(model.file)))
        result = model.run()
        return result
    else:
        raise ModelExceptions.NotAllowedAccess()