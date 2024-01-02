from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ModelSerializer
from .models import Models
from shutil import rmtree
from APIUsers import settings
from .auth import authenticate
from .modelExecutionViews import loadModel
import os

class ModelView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            request.data['id_user'] = payload['id']
            serializer = ModelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            try:
                model = Models.objects.filter(pk=serializer.data['id']).first()
                loadModel(os.path.join(settings.MEDIA_ROOT,str(model.file)))
                return Response(serializer.data)
            except Exception:
                self.delete(self,serializer.data)
                response = Response()
                response.status_code=400
                response.data = {
                    'message': 'The model was not correctly defined'
                }
                return response
        except AuthenticationFailed as authFailed:
            raise authFailed
    
    def get(self,request,modelId=-1):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            if(modelId == -1):
                models = Models.objects.filter(id_user=payload['id'])
                result = []
                for model in models:
                    serializer = ModelSerializer(model)
                    result.append(serializer.data)
                return Response(result)
            else:
               model = Models.objects.filter(id_user=payload['id'], id=modelId).first()
               if(model is not None):
                    serializer = ModelSerializer(model)
                    return Response(serializer.data)
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
            model = Models.objects.filter(id_user=payload['id'], id=request.data['id']).first()
            serializer = ModelSerializer(model)
            rmtree(os.path.join(settings.MEDIA_ROOT, "models", str(serializer.data['id_user']), serializer.data['name']))
            model.delete()
            response = Response()
            response.data = {
            'message': 'Model deleted succesfully'
            }
            return response
        except AuthenticationFailed as authFailed:
            print(token)
            raise authFailed
        except Exception as e:
            print(e)
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
            model = Models.objects.filter(id_user=payload['id'], pk=request.data['id']).first()
            if model.image != request.data['image']:
                os.remove(os.path.join(settings.MEDIA_ROOT,str(model.image)))
                model.image=request.data['image']
            if model.file != request.data['file']:
                os.remove(os.path.join(settings.MEDIA_ROOT,str(model.file)))
                model.file=request.data['file']
            if model.name != request.data['name']:
                url = os.path.join(settings.MEDIA_ROOT, "models", str(payload['id']))
                os.rename(os.path.join(url,model.name),os.path.join(url,request.data['name']))
                model.name=request.data['name']
            model.save()
            serializer = ModelSerializer(model)
            return Response(serializer.data)
        except AuthenticationFailed as authFailed:
            raise authFailed
        except Exception as e:
            response = Response()
            response.data = {
            'message': e
            }
            return response