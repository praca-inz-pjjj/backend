from backbone.models import CustomUser
from backbone.permisions import IsTeacher
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backbone.serializers import CustomUserSerializer, PermittedUserSerializer
from parent_panel.models import Permission, PermittedUser
from parent_panel.serializers import PermissionSerializer
from datetime import datetime

from teacher_panel.models import Children
from teacher_panel.serializers import ChildrenSerializer


class AcceptReceiptView(APIView):
    permission_classes = [IsTeacher]
    def get(self, request):
        try:
            id = request.GET.get('id')
            permision = Permission.objects.get(qr_code = id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            permisionSerializer = PermissionSerializer(permision)
            if permisionSerializer['state'].value == 'ACTIVE':
                start_date = datetime.fromisoformat(permisionSerializer['start_date'].value)
                end_date = datetime.fromisoformat(permisionSerializer['end_date'].value)
                current = datetime.now(start_date.tzinfo)
                
                if start_date < current and end_date > current:
                    parent = CustomUser.objects.get(id = permisionSerializer.data['parent'])
                    parentSerializer = CustomUserSerializer(parent)
                    
                    permittedUser = PermittedUser.objects.get(id = permisionSerializer.data['permitteduser'])
                    permittedUserSerializer = PermittedUserSerializer(permittedUser)

                    child = Children.objects.get(id = permittedUserSerializer.data['child'])
                    childSerializer = ChildrenSerializer(child)

                    reciver = CustomUser.objects.get(id = permittedUserSerializer.data['user'])
                    reciverSerializer = CustomUserSerializer(reciver)

                    return Response({ 'id': id, 'permission': permisionSerializer.data, 
                                    'parent': parentSerializer.data, 'reciver': reciverSerializer.data, 'child': childSerializer.data})
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)