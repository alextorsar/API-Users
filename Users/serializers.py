from rest_framework import serializers
from .models import Users, Models, SubModels

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Models
        fields = ['id', 'name', 'id_user', 'image', 'file']
        
class SubModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubModels
        fields = ['id', 'id_model', 'file']