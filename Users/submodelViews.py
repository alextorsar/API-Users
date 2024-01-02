from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import SubModelSerializer
from .models import Models, SubModels
from APIUsers import settings
from .auth import authenticate
from os import remove
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
        
    def get(self, request):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            parentModel = Models.objects.filter(id_user=payload['id'], id=request.data['id_model']).first()
            if(parentModel is not None):
                submodels = SubModels.objects.filter(id_model=request.data['id_model'])
                result = []
                for submodel in submodels:
                    serializer = SubModelSerializer(submodel)
                    result.append(serializer.data)
                return Response(result)
            else:
                response = Response()
                response.status_code = 403
                response.data = {
                'message': 'You are not allowed to get submodels from this model'
                }
                return response
        except AuthenticationFailed as authFailed:
            raise authFailed
    
    def delete(self,request):
        token = request.COOKIES.get('jwt')
        try:
            payload = authenticate(token)
            submodel = SubModels.objects.filter(id=request.data['id']).first()
            parentModel = Models.objects.filter(id_user=payload['id'], id=submodel.id_model.id).first()
            if(parentModel is not None):
                os.remove(os.path.join(settings.MEDIA_ROOT,str(submodel.file)))
                submodel.delete()
                response = Response()
                response.data = {
                'message': 'Model deleted succesfully'
                }
                return response
            else:
                response = Response()
                response.status_code = 403
                response.data = {
                'message': 'You are not allowed to remove this submodel'
                }
        except AuthenticationFailed as authFailed:
            raise authFailed
        except Exception as e:
            #response = Response()
            #response.status_code = 400
            #response.data = {
            #'message': 'Submodel could not be deleted'
            #}
            #return response
            raise e
        

    
    