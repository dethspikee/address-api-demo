from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from .serializers import UserSerializer, AddressSerializer
from .models import User


class AddressView(ListCreateAPIView):

    serializer_class = AddressSerializer

    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
        except ValidationError as e:
            return Response({"field_error": e}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            return Response({"field_error": "User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user_id=user.id)
            except ValidationError as e:
                return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
