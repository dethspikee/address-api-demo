from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, AddressSerializer
from .models import User


class AddressView(APIView):
    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    
    def post(self, request):
        user_uuid = request.data.get("user_uuid")
        if not user_uuid:
            error_message = {
                "error": {
                    "type": "Missing field.",
                    "message": "user_uuid missing."
                }
            }
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(user_uuid=user_uuid)
        except ValidationError as e:
            return Response({"field_error": e}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            return Response({"field_error": "User with such UUID doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AddressSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
