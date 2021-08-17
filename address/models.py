import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
            related_name='address')
    street = models.CharField(max_length=250, blank=False)
    postcode = models.CharField(max_length=30, blank=False)
    town = models.CharField(max_length=30, blank=False)
    country = models.CharField(max_length=30, blank=False)
    current = models.BooleanField()

    class Meta:
        unique_together = ['street', 'postcode', 'town', 'country']

    def __str__(self):
        return f'Address for user: {self.user.first_name}'
