from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                'username',
                'email',
                'first_name',
                'last_name',
                'is_active',
                'is_superuser',
                'is_staff',
                'last_login',
                'date_joined']
