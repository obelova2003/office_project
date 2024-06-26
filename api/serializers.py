from rest_framework import serializers
from .models import OfficeUser, Report, Application

from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class OfficeUsersSerializer(serializers.ModelSerializer):
    is_manager = serializers.SerializerMethodField(method_name = 'get_is_manager')
    is_client = serializers.SerializerMethodField(method_name = 'get_is_client')
    is_director = serializers.SerializerMethodField(method_name = 'get_is_director')


    class Meta:
        model = OfficeUser
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 
                  'is_manager', 'is_client', 'is_director')
        read_only_fields = ('last_login', 'is_superuser', 
                            'is_staff', 'is_active', 'date_joined', 'manager')
        
    def get_is_manager(self, obj):
        return obj.is_manager

    def get_is_client(self, obj):
        return obj.is_client
    
    def get_is_director(self, obj):
        return obj.is_director


class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeUser
        fields = '__all__'
        read_only_fields = ('last_login', 'is_superuser', 
                            'is_staff', 'is_active', 'date_joined', 'manager', 'groups', 'user_permissions')


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeUser
        fields = '__all__'
        read_only_fields = ('last_login', 'is_superuser', 
                             'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ('id',  'number', 'title', 'storage_name_from', 'storage_name_to', 'count')
        read_only_fields = ( 'author_client', 'status', )

    def create(self, validated_data):
        request = self.context.get('request')
        office_user = OfficeUser.objects.get(username=request.user)
        validated_data['author_client'] = office_user
        validated_data['status'] = 'created'
        return super().create(validated_data)
    

class ApplicationGetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
