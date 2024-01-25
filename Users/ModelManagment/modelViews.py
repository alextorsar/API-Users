from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from ..serializers import ModelSerializer
from ..models import Models
from APIUsers import settings
from ..auth import authenticate
from ..ModelManagment import modelController
import os

class ModelView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        try:
            print(request.data)
            payload = authenticate(token)
            request.data['id_user'] = payload['id'] 
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
            modelController.deleteModel(request.data['id'],payload['id'])
            response = Response()
            response.data = {
            'message': 'Model deleted succesfully'
            }
            return response
        except AuthenticationFailed as authFailed:
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