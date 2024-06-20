from rest_framework import serializers

from .models import OfficeUser

class OfficeUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeUser
        fields = '__all__'
        read_only_fields = ('last_login', 'is_superuser', 
                            'is_staff', 'is_active', 'date_joined', )