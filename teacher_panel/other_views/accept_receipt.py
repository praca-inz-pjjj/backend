import json
from backbone.models import CustomUser, Log
from backbone.permisions import IsIssuer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backbone.serializers import CustomUserSerializer, PermittedUserSerializer
from backbone.types import LogType, PermissionState
from parent_panel.models import History, Permission, PermittedUser
from parent_panel.serializers import HistorySerializer, PermissionSerializer
from datetime import datetime
from django.utils import timezone

from teacher_panel.models import Child
from teacher_panel.serializers import ChildrenSerializer


class AcceptReceiptView(APIView):
    permission_classes = [IsIssuer]
    def get(self, request):
        try:
            id = request.GET.get('id')
            byId = request.GET.get('byId')
            if byId == '1':
                permision = Permission.objects.get(id=id)
            else:
                permision = Permission.objects.get(qr_code = id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            permisionSerializer = PermissionSerializer(permision)
            if permisionSerializer['state'].value == 'ACTIVE' or permisionSerializer['state'].value == 'PERMANENT' or byId == '1':
                start_date = datetime.fromisoformat(permisionSerializer['start_date'].value)
                end_date = datetime.fromisoformat(permisionSerializer['end_date'].value)
                current = datetime.now(start_date.tzinfo)
                
                if (start_date < current and end_date > current) or permisionSerializer['state'].value == 'PERMANENT':
                    parent = CustomUser.objects.get(id = permisionSerializer.data['parent'])
                    parentSerializer = CustomUserSerializer(parent)
                    
                    permittedUser = PermittedUser.objects.get(id = permisionSerializer.data['permitteduser'])
                    permittedUserSerializer = PermittedUserSerializer(permittedUser)

                    child = Child.objects.get(id = permittedUserSerializer.data['child'])
                    childSerializer = ChildrenSerializer(child)

                    reciver = CustomUser.objects.get(id = permittedUserSerializer.data['user'])
                    reciverSerializer = CustomUserSerializer(reciver)

                    return Response({ 'id': id, 'permission': permisionSerializer.data, 
                                    'parent': parentSerializer.data, 'reciver': reciverSerializer.data, 'child': childSerializer.data})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            permission_id = data.get('permission_id')
            acceptance = data.get('acceptance')
            receiver_id = data.get('reciver_id')
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            permission = Permission.objects.get(id = permission_id)
            permissionSerializer = PermissionSerializer(permission)

            if permissionSerializer['state'].value == 'ACTIVE' or permissionSerializer['state'].value == 'SLEEP' or permissionSerializer['state'].value == 'PERMANENT':

                permittedUser = PermittedUser.objects.get(id = permissionSerializer.data['permitteduser'])
                permittedUserSerializer = PermittedUserSerializer(permittedUser)

                if str(permittedUserSerializer.data['user']) != str(receiver_id):
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                historySerializer = HistorySerializer(data = {'child': permittedUserSerializer.data['child'], 'receiver': permittedUserSerializer.data['user'], 'teacher': request.user.id, 'decision': acceptance, 'date': timezone.now()})

                if historySerializer.is_valid():
                    history = historySerializer.save()
                    if permission.state != PermissionState.PERMANENT:
                        permission.state = PermissionState.CLOSED
                        permission.save()
                    Log.objects.create(log_type=LogType.CREATE, data={"type" : "History", "history_id" : history.id, "receiver_id" : receiver_id, "child_id" : permittedUserSerializer.data['child']})
                    return Response(status=status.HTTP_204_NO_CONTENT)
                
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)