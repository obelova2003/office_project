from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from api.models import OfficeUser
from api import serializers

from django.contrib.auth.hashers import make_password

class OfficeUserViewSet(viewsets.ModelViewSet):
    queryset = OfficeUser.objects.all()
    serializer_class = serializers.OfficeUsersSerializer

    http_method_names = ['get', 'post']

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        # print(request.data['password'])
        password = request.data['password']
        hashed_password = make_password(password)
        request.data._mutable = True
        request.data['password'] = hashed_password
        request.data._mutable = False
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
