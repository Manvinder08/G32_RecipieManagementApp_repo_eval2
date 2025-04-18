from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    img_url = models.URLField()
    overview = models.TextField()
    ingredients = models.TextField(help_text="Comma-separated list of ingredients")
    time_to_prepare = models.CharField(max_length=50)
    full_process = models.TextField()
    is_veg = models.BooleanField(default=True) 

    def __str__(self):
        return self.title

