from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'postcode', 'town', 'country')


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False, read_only=False)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'address')
