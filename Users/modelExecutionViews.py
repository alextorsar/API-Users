from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ModelSerializer
from .models import Models
import pysd
from APIUsers import settings
import os.path
from json import loads, dumps
from .auth import authenticate

def getModelFromPath(modelPath):
    file, extension = os.path.splitext(modelPath)
    path = file + ".py"
    return pysd.load(path)

def loadModel(modelPath):
    file, extension = os.path.splitext(modelPath)
    try:
        if extension == '.xmile':
            pysd.read_xmile(modelPath)
        elif extension == '.mdl':
            pysd.read_vensim(modelPath)
        else:
            raise ValueError('The file extension is not valid')
    except Exception as e:
        raise e

class ModelDocumentationView(APIView):
    def get(self,request,modelId=-1):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            if (modelId!=-1):
                model = Models.objects.filter(id_user=payload['id'], id=modelId).first()
                try:
                    model = getModelFromPath(os.path.join(settings.MEDIA_ROOT,str(model.file)))
                    result = model.doc.to_json(orient="records")
                    parsed = loads(result)
                    return Response(dumps(parsed, sort_keys=True, indent=4, separators=(',',': ')))
                except:
                    response = Response()
                    response.status_code=400
                    response.data = {
                        'message': 'The path was not correct'
                    }
                    return response
        except AuthenticationFailed as authFailed:
            raise authFailed


