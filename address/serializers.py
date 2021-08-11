from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('postcode', 'town')


class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        depth = 1
        fields = ('username', 'addresses',)
