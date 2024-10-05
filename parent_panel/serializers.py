from rest_framework_simplejwt.serializers import serializers
from .models import History, Permission, UserChildren
class PartialUserChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChildren
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'