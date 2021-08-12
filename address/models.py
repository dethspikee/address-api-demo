from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
            related_name='address', primary_key=True)
    street = models.CharField(max_length=250)
    postcode = models.CharField(max_length=30)
    town = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    current = models.BooleanField()
