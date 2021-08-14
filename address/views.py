from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, AddressSerializer2, AddressSerializer
from .models import User


class AddressView(APIView):

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AddressSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=2)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
