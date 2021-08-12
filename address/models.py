from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
            related_name='address')
    street = models.CharField(max_length=250)
    postcode = models.CharField(max_length=30)
    town = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    current = models.BooleanField()

    def __str__(self):
        return f'Address for user: {self.user.first_name}'
