from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Address, User


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'postcode', 'town', 'country', 'current')


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'address')


class AddressSerializer2(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    street = serializers.CharField(required=False, allow_blank=True,
            max_length=200)
    postcode = serializers.CharField(required=False, allow_blank=True,
            max_length=200)
    town = serializers.CharField(required=False, allow_blank=True,
            max_length=200)
    country = serializers.CharField(required=False, allow_blank=True,
            max_length=200)
    current = serializers.BooleanField(required=False)

    def create(self, validated_data):
        return Address.objects.create(**validated_data)
