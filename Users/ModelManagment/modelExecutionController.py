from ..models import Models
import pysd
from APIUsers import settings
import os.path, os
import math
from ..exceptions import ModelExceptions,ModelExecutionExceptions
import pandas as pd
import shutil
import json

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

def getFileFromChunks(file, name):
    with open(name, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return name

def transformParamsFunctionsToPandasSeries(params, files, temporaryPath):
    for key in params:
        if params[key]['type'] == "FileObject":
            name = os.path.join(temporaryPath, params[key]['name'])
            extension = os.path.splitext(name)[1]
            if extension in ['.xlsx', '.xls']:
                excelFilePath = getFileFromChunks(files['params[{}]'.format(key)], name)
                excelDataFrame = pd.read_excel(excelFilePath)
                if 'xpts' in excelDataFrame.columns and 'ypts' in excelDataFrame.columns:
                    params[key] = pd.Series(index=excelDataFrame['xpts'].tolist(), data=excelDataFrame['ypts'].tolist())
                else:
                    raise ModelExecutionExceptions.IncorrectExcelFile()
            else:
                raise ModelExecutionExceptions.IncorrectExcelFileExtension()
    return params
    
def getModelExecutionResult(modelId,userId,executionConditions, files):
    temporaryPath = os.path.join(settings.MEDIA_ROOT, 'temp', str(modelId))
    os.makedirs(temporaryPath)
    try:
        model = Models.objects.filter(id_user=userId, id=modelId).first()
        params = json.loads(executionConditions['params'])
        initial_condition = json.loads(executionConditions['initial_condition'])
        start_time = int(executionConditions['start_time'])
        params = transformParamsFunctionsToPandasSeries(params, files, temporaryPath)
        if model is not None:
            model = getModelFromPath(os.path.join(settings.MEDIA_ROOT,str(model.file)))
            result = model.run(initial_condition=(start_time,initial_condition),params=params)
            return result
        else:
            raise ModelExceptions.NotAllowedAccess()
    finally:
        shutil.rmtree(temporaryPath)