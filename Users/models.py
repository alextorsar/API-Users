from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
    name = models.CharField(max_length=50)
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username', 'password']