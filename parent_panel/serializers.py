from rest_framework_simplejwt.serializers import serializers

from teacher_panel.models import Children
from .models import History, Permission, UserChildren, PermittedUser


class UserChildrenSerializer(serializers.ModelSerializer):
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

class PermittedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermittedUser
        fields = '__all__'

class ParentChildrenSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)  # Get classroom name

    class Meta:
        model = Children
        fields = ['id', 'name', 'surname', 'classroom_name']

class HistorySerializer(serializers.ModelSerializer):
    child_name = serializers.CharField(source='child.name', read_only=True)  # Get child name
    child_surname = serializers.CharField(source='child.surname', read_only=True)  # Get child name
    receiver_name = serializers.CharField(source='receiver.first_name', read_only=True)  # Get receiver name
    receiver_surname = serializers.CharField(source='receiver.last_name', read_only=True)  # Get receiver name
    teacher_name = serializers.CharField(source='teacher.first_name', read_only=True)  # Get teacher name
    teacher_surname = serializers.CharField(source='teacher.last_name', read_only=True)  # Get teacher name

    class Meta:
        model = History
        fields = '__all__'