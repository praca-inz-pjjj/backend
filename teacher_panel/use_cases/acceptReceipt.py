from backbone.models import CustomUser
from backbone.permisions import IsTeacher
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backbone.serializers import CustomUserSerializer
from parent_panel.models import Permission
from parent_panel.serializers import PermissionSerializer


class AcceptReceiptView(APIView):
    permission_classes = [IsTeacher]
    def get(self, request):
        try:
            id = request.GET.get('id')
            print(id)
            permision = Permission.objects.get(qr_code = id)
            if not permision:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            print(permision)
            permisionSerializer = PermissionSerializer(permision)
            print(permisionSerializer)
            if permisionSerializer['state'].value == 'ACTIVE':
                parent = CustomUser.objects.get(id = permisionSerializer.data['parent'])
                # permittedUser = CustomUser.objects.get()
                parentSerializer = CustomUserSerializer(parent)
                print('ma permisje')
                return Response({ 'id': id, 'permission': permisionSerializer.data, 
                                 'parent': parentSerializer.data})
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)