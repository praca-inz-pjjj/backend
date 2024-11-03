from rest_framework_simplejwt.serializers import serializers

from teacher_panel.models import Child
from .models import History, Permission, UserChild, PermittedUser


class UserChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChild
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

class PermittedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermittedUser
        fields = '__all__'

class ParentChildrenSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)  # Get classroom name

    class Meta:
        model = Child
        fields = ['id', 'name', 'surname', 'classroom_name']