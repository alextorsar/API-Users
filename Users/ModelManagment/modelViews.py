from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from ..serializers import ModelSerializer
from ..models import Models, Users
from APIUsers import settings
from ..auth import authenticate
from ..ModelManagment import modelController
import os
from APIUsers.settings import ONLY_ADMIN_CAN_CREATE_MODELS

class ModelView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            request.data['id_user'] = payload['id']
            if(ONLY_ADMIN_CAN_CREATE_MODELS):
                user = Users.objects.filter(id=payload['id']).first()
                if(not user.admin):
                    raise AuthenticationFailed('Only admin can create models')
            try:
                model = modelController.createModel(request) 
                return Response(model)
            except Exception as e:
                raise e
        except AuthenticationFailed as authFailed:
            raise authFailed
    
    def get(self,request,modelId=-1):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            if(modelId == -1):
                models = modelController.getUserModels(payload['id'])
                return Response(models)
            else:
                model = modelController.getModel(payload['id'], modelId)
                if(model is not None):
                    return Response(model)
                else:
                    response = Response()
                    response.status_code=400
                    response.data = {
                        'message': 'Model not found'
                    }
                    return response         
        except AuthenticationFailed as authFailed:
            raise authFailed
    
    def delete(self, request):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            if ONLY_ADMIN_CAN_CREATE_MODELS:
                user = Users.objects.filter(id=payload['id']).first()
                if(not user.admin):
                    raise AuthenticationFailed('Only admin can delete models')
            modelController.deleteModel(request.data['id'],payload['id'])
            response = Response()
            response.data = {
            'message': 'Model deleted succesfully'
            }
            return response
        except AuthenticationFailed as authFailed:
            raise authFailed
        except Exception as e:
            response = Response()
            response.status_code = 400
            response.data = {
            'message': 'Model could not be deleted'
            }
            return response
        
    def put(self, request):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            if ONLY_ADMIN_CAN_CREATE_MODELS:
                user = Users.objects.filter(id=payload['id']).first()
                if(not user.admin):
                    raise AuthenticationFailed('Only admin can update models')
            newModel = modelController.updateModel(request.data,payload['id'])
            return Response(newModel)
        except AuthenticationFailed as authFailed:
            raise authFailed
        except Exception as e:
            response = Response()
            response.data = {
            'message': 'Model could not be updated'
            }
            response.status_code = 400
            return response