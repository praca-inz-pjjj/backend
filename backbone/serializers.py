from rest_framework_simplejwt.serializers import serializers

from parent_panel.models import PermittedUser
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']

class PermittedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermittedUser
        fields = '__all__'