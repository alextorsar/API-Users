from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from ..serializers import SubModelSerializer
from ..models import Models, SubModels
from APIUsers import settings
from ..auth import authenticate
from os import remove
from .subModelController import getSubModelsFromModel, deleteSubModel
import os

class SubModelView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            parentModel = Models.objects.filter(id_user=payload['id'], id=request.data['id_model']).first()
            if (parentModel is not None):
                serializer = SubModelSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                response = Response()
                response.status_code = 403
                response.data = {
                'message': 'You are not allowed to create submodels for this model'
                }
                return response
        except AuthenticationFailed as authFailed:
            raise authFailed
        
    def get(self,request , modelId=-1):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            if (modelId != -1):
                subModels = getSubModelsFromModel(payload['id'],modelId)
                if (subModels is not None):
                    return Response(subModels)
                else:
                    response = Response()
                    response.status_code = 403
                    response.data = {
                    'message': 'You are not allowed to get submodels from this model'
                    }
                    return response
            else:
                response = Response()
                response.status_code = 400
                response.data = {
                'message': 'Parent model id is required'
                }
                return response
        except AuthenticationFailed as authFailed:
            raise authFailed
    
    def delete(self,request):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            try:
                deleteSubModel(request.data['id'], payload['id'])
                response = Response()
                response.status_code = 200
                response.data = {
                    'message': 'Submodel was deleted successfully'
                }
                return response
            except Exception as e:
                raise e  
        except AuthenticationFailed as authFailed:
            raise authFailed
        except Exception as e:
            response = Response()
            response.status_code = 400
            response.data = {
            'message': 'Submodel could not be deleted'
            }
            return response