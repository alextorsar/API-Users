from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from ..auth import authenticate
from .modelExecutionController import getModelDocumentation, getModelExecutionResult
import json

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
                        'message': e
                    }
                    return response
        except AuthenticationFailed as authFailed:
            raise authFailed
        
class ModelExecutionView(APIView):
    def post(self,request,modelId=-1):
        executionConditions = json.loads(request.data['executionConditions'])
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            if (modelId!=-1):
                try:
                    result = getModelExecutionResult(modelId,payload['id'],executionConditions)
                    return Response(result)
                except Exception as e:
                    response = Response()
                    response.status_code=400
                    response.data = {
                        'message': e
                    }
                    return response
        except AuthenticationFailed as authFailed:
            raise authFailed


