from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username', 'password']

def generate_image_dirname(self, filename):
    url = "models/{}/{}/image/{}".format(self.id_user.id, self.name, filename)
    return url
def generate_files_dirname(self, filename):
    url = "models/{}/{}/files/{}".format(self.id_user.id, self.name, filename)
    return url
def get_parent_model_dirname(self, filename):
    parentModel = Models.objects.filter(id=self.id_model.id).first()
    url = "models/{}/{}/files/{}".format(parentModel.id_user.id, parentModel.name, filename)
    return url


class Models(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    id_user=models.ForeignKey(Users,null=False,blank=False, on_delete=models.CASCADE)
    image=models.ImageField(upload_to= generate_image_dirname, null=False)
    file=models.FileField(upload_to= generate_files_dirname, null=False, validators=[FileExtensionValidator(allowed_extensions=["xmile","mdl"])])
    class Meta:
        unique_together = ('id_user','name')

class SubModels(models.Model):
    id=models.AutoField(primary_key=True)
    id_model=models.ForeignKey(Models,null=False,blank=False, on_delete=models.CASCADE)
    file=models.FileField(upload_to= "models/1/model5/files/", null=False, validators=[FileExtensionValidator(allowed_extensions=["xmile","mdl"])])
    

    