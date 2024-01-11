from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from ..auth import authenticate
from .modelExecutionController import getModelDocumentation,NotAllowedAccess, IncorrectModelDefinition, IncorrectFileExtension, IncorrectModelPath

class ModelDocumentationView(APIView):
    def get(self,request,modelId=-1):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            if (modelId!=-1):
                try:
                    result = getModelDocumentation(modelId,payload['id'])
                    return Response(result)
                except Exception as e:
                    response = Response()
                    response.status_code=400
                    response.data = {
                        'message': e.message
                    }
                    return response
        except AuthenticationFailed as authFailed:
            raise authFailed


