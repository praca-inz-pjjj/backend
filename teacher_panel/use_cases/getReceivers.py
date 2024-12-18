from pyclbr import Class
from django.utils import timezone
from backbone.models import CustomUser, Log
from backbone.permisions import IsTeacher
from backbone.serializers import CustomUserSerializer, PermittedUserSerializer
from backbone.types import LogType, PermissionState
from parent_panel.models import Permission, PermittedUser, UserChild
from parent_panel.serializers import UserChildrenSerializer, PermissionSerializer
from teacher_panel.models import Child, Classroom
from teacher_panel.serializers import ChildrenSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class GetReceiversView(APIView):
    permission_classes = [IsTeacher]
    def get(self, request):
        try:
            receivers = CustomUser.objects.filter(parent_perm__range=(1,2))
            receivers_serializer = CustomUserSerializer(receivers, many=True)
            return Response(receivers_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)