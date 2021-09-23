from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.mixins import UpdateModelMixin, ListModelMixin,\
RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from dj_rest_auth.registration.views import RegisterView

from .serializers import AddressSerializer
from .models import User, Address
from .permissions import OwnerOnly
from .custom_drf_responses import register_response


class AddressRegister(RegisterView):
    
    @swagger_auto_schema(operation_description="Register new user",
            security=[], responses=register_response)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class AddressDetail(RetrieveAPIView):

    serializer_class = AddressSerializer
    permission_classes = [OwnerOnly]

    @swagger_auto_schema(operation_description="Retrieve single address", security=[
        {"Token": []}
    ])
    def get(self, request, pk, *args, **kwargs):
        address = self.get_object(pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Update address", security=[
        {"Token": []}
    ])
    def patch(self, request, pk,  *args, **kwargs):
        address = self.get_object(pk)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete address", security=[
        {"Token": []}
    ])
    def delete(self, request, pk, *args, **kwargs):
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        obj = get_object_or_404(Address, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj


current_param = openapi.Parameter('current', openapi.IN_QUERY,
        description="Filter out addresses based on the 'current' attribute.", type=openapi.TYPE_BOOLEAN)
postcode_param = openapi.Parameter('postcode', openapi.IN_QUERY,
        description="Retrieve addresses with a given postcode", type=openapi.TYPE_STRING)
class AddressesView(ListCreateAPIView, CreateModelMixin):

    serializer_class = AddressSerializer

    @swagger_auto_schema(
        manual_parameters=[current_param, postcode_param],
        operation_description="List all addresses", security=[
        {"Token": []}
    ])
    def get(self, request, format=None):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Create new address", security=[
        {"Token": []}
    ])
    def post(self, request):
        try:
            return super().post(request)
        except ValidationError as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.filter(user_id=user.id)
        index = {"true": True, "false": False}
        current = self.request.query_params.get("current")
        street = self.request.query_params.get("street")
        town = self.request.query_params.get("town")
        postcode = self.request.query_params.get("postcode")
        country = self.request.query_params.get("country")

        if current is not None and current in index:
            queryset = queryset.filter(current=index[current])

        if street:
            queryset = queryset.filter(street__iexact=street)

        if town:
            queryset = queryset.filter(town__iexact=town)

        if postcode:
            queryset = queryset.filter(postcode__iexact=postcode)

        if country:
            queryset = queryset.filter(country__iexact=country)

        return queryset
