from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer
from .models import User


class AddressView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    print("queryset: ", queryset)
    serializer_class = UserSerializer
