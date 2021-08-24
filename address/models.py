from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
            related_name='address')
    street = models.CharField(max_length=250, blank=False)
    postcode = models.CharField(max_length=30, blank=False)
    town = models.CharField(max_length=30, blank=False)
    country = models.CharField(max_length=3, blank=False)
    current = models.BooleanField()

    class Meta:
        unique_together = ['street', 'postcode', 'town', 'country']

    def save(self, *args, **kwargs):
        if self.current and Address.objects.filter(user_id=self.user_id,
                current=True).exists():
            raise ValidationError("Cannot create another address with 'current'"
                    " set to True!")
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f'Address for user: {self.user.first_name}'
