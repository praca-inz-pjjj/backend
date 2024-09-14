from rest_framework_simplejwt.serializers import serializers
from .models import UserChildren
class UserChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChildren
        fields = '__all__'