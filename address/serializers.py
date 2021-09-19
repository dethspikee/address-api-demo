import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from dj_rest_auth.serializers import TokenSerializer
from dj_rest_auth.models import TokenModel

from .models import Address, User


class MyTokenSerializer(TokenSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        model = TokenModel
        fields = ("username",)


class AddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.ReadOnlyField(source="user.first_name")
    street = serializers.CharField(max_length=200)
    postcode = serializers.CharField(max_length=200)
    town = serializers.CharField(max_length=200)
    country = serializers.CharField(max_length=3)
    current = serializers.BooleanField(required=False)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Address.objects.all(),
                fields=['street', 'postcode', 'town', 'country']
            )
        ]

    def validate_street(self, value):
        return re.sub("\s+", " ", value)

    def validate_postcode(self, value):
        return re.sub("\s+", " ", value)

    def validate_town(self, value):
        return re.sub("\s+", " ", value)

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.street = validated_data.get("street", instance.street)
        instance.country = validated_data.get("country", instance.country)
        instance.town = validated_data.get("town", instance.town)
        instance.postcode = validated_data.get("postcode", instance.postcode)
        instance.current = validated_data.get("current", instance.current)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True, read_only=False)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'address')

