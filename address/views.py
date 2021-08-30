from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.mixins import UpdateModelMixin, ListModelMixin,\
RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from .serializers import AddressSerializer
from .models import User, Address


class AddressDetail(RetrieveAPIView):

    serializer_class = AddressSerializer

    def get(self, request, pk, *args, **kwargs):
        address = self.get_object(pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def patch(self, request, pk,  *args, **kwargs):
        address = self.get_object(pk)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        return get_object_or_404(Address, pk=pk)


class AddressView(ListCreateAPIView, CreateModelMixin):

    serializer_class = AddressSerializer

    def get(self, request, format=None):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data)

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
