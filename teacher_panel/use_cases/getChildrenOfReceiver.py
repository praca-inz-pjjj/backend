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
from django.utils.timezone import now

class GetChildrenOfReceiverView(APIView):
    permission_classes = [IsTeacher]
    def get(self, request, id):
        try:
            permittedusers = PermittedUser.objects.filter(user_id=id)
            permissions = Permission.objects.filter(
            permitteduser__in=permittedusers,
            state__in=['SLEEP', 'ACTIVE'],
            start_date__lte=now(),
            end_date__gte=now()
            ).union(Permission.objects.filter(permitteduser__in=permittedusers,
            state='PERMANENT'))
            obj = []
            permissionSerializer = PermissionSerializer(permissions, many=True)
            for permission in permissionSerializer.data:
                permitteduser = PermittedUser.objects.get(id=permission['permitteduser'])
                permitteduserSerializer = PermittedUserSerializer(permitteduser)
                child = Child.objects.get(id=permitteduserSerializer.data['child'])
                childrenSerializer = ChildrenSerializer(child)
                obj.append({'permission': permission, 'child': childrenSerializer.data})
            return Response({'objects': obj}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)