from rest_framework_simplejwt.serializers import serializers
from .models import Permission, UserChildren
class PartialUserChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChildren
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'