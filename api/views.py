from datetime import time
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import viewsets, status
from api.models import OfficeUser, Report, Application, Storage
from api import serializers
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.move_storage import move
from api.permissions import ManagerRole, ClientRole, CanSeeApplications, DirectorRole
from api.filters import ApplicationFilter
from api.exceptions import PermissionDeniedException
from django_filters.rest_framework import DjangoFilterBackend

import threading

class OfficeUserViewSet(viewsets.ModelViewSet):
    queryset = OfficeUser.objects.all()
    serializer_class = serializers.OfficeUsersSerializer

    http_method_names = ['get', 'post']

    def hash_password(self, data):
        password = data.get('password')
        data['password'] = make_password(password)
        return data

    def get_serializer_class(self):        
        if self.action == "manager_create":
            return serializers.ManagerSerializer
        elif self.action == "client_create":
            return serializers.ClientSerializer
        else:
            return serializers.OfficeUsersSerializer

    @action(
        methods=['POST',],
        detail=False,
    )
    def manager_create(self, request):
        data = self.hash_password(request.data.copy())
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

    @action(
        methods=['POST',],
        detail=False,
    )
    def client_create(self, request):
        data = self.hash_password(request.data.copy())
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.LoginSerializer

    @action(
        methods=['POST',],
        detail=False,
        permission_classes=(AllowAny,)
    )
    def login(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = OfficeUser.objects.get(username=serializer.validated_data.get('username'))
        except OfficeUser.DoesNotExist as e:
            raise serializers.ValidationError(str(e))
        refresh = RefreshToken.for_user(user)
        token_data={}
        token_data['id'] = user.id
        token_data['refresh'] = str(refresh)
        token_data['access'] = str(refresh.access_token)
        return Response(token_data, status=status.HTTP_200_OK)
        

class LogoutViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.LogoutSerializer

    @action(
        methods=['POST',],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def logout(self, request):
        Refresh_token = request.data["refresh"]
        token = RefreshToken(Refresh_token)
        token.blacklist()
        return Response({"message": "Токен удален"}, status=status.HTTP_200_OK)
    

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = serializers.ReportSerializer
    permission_classes = (ManagerRole, )

    http_method_names = ['get', 'post', 'delete']

    def list(self, request):
        return Response(serializers.ReportSerializer(Report.objects.all(), many=True).data)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicationFilter

    http_method_names = ['get', 'post', 'patch', 'put']
    
    def get_serializer_class(self):        
        if self.action == "inwork":
            return serializers.ApplicationStatusSerializer
        else:
            return serializers.ApplicationSerializer
        
        
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [CanSeeApplications]
        elif self.action == 'inwork' or self.action == 'executed':
            permission_classes=[ManagerRole]
        else:
            permission_classes = [ClientRole]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        if request.user.role == 'client':
            if not self.request.query_params:
                user = request.user
                queryset = Application.objects.filter(author_client=user).select_related('author_client')
                serializer = serializers.ApplicationGetSerializers(queryset, many=True)
                return Response(serializer.data)
            else:
                raise PermissionDeniedException
        elif self.request.user.role == 'manager':
            manager_clients = OfficeUser.objects.filter(manager=request.user).prefetch_related('application_set')
            author_clients = [c.id for c in manager_clients]
            params = []
            if self.request.query_params:
                params = (dict(self.request.query_params))['author_client']
                params = list(map(int, params))
            if [i for i in params if i in author_clients] or (not self.request.query_params):
                queryset = Application.objects.filter(author_client__in=[c.id for c in manager_clients])
                queryset = self.filter_queryset(queryset)
                serializer = serializers.ApplicationGetSerializers(queryset, many=True)
                return Response(serializer.data)
            else:
                raise PermissionDeniedException
        else:
            queryset = self.filter_queryset(self.queryset)
            serializer = serializers.ApplicationGetSerializers(queryset, many=True)
            return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


    @action(
        methods=['PUT'],
        detail=True,
        url_path='inwork',
    )
    def inwork(self, request, pk=None):
        application = get_object_or_404(Application, pk=pk)
        manager_clients = OfficeUser.objects.filter(manager_id=request.user.id)
        author_clients = [c.id for c in manager_clients]
        if application.author_client.id in author_clients and application.status == 'created':
            application.status = 'inwork'
            application.save()
            storage_to = get_object_or_404(Storage, name = application.storage_name_to)
            storage_from = get_object_or_404(Storage, name = application.storage_name_from)
            move_thread = threading.Thread(target=move, 
                                       args=(storage_to, storage_from, application))
            move_thread.start()
            return Response({"message": f"Статус заявки обновлен на 'в работе'!"}, status=status.HTTP_200_OK)
        else:
            raise PermissionDeniedException
        

class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = serializers.StorageSerializer
    permission_classes = (DirectorRole, )

    http_method_names = ['get', 'post']

    def list(self, request):
        return Response(serializers.StorageSerializer(Storage.objects.all(), many=True).data)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
