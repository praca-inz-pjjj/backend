from urllib.request import Request

from backbone.models import CustomUser
from backbone.permisions import IsParent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backbone.serializers import CustomUserSerializer
from parent_panel.models import PermittedUser, UserChild

class ReceiverPermission(APIView):
    permission_classes = (IsParent, )
    def get(self, request: Request):
        try:
            parent: CustomUser = request.user
        
            users = CustomUser.objects.filter(parent_perm__in=[1,2]).exclude(id=parent.id)
            usersSerializer = CustomUserSerializer(users, many=True)
            return Response(data=usersSerializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def post(self, request: Request):
        try:
            parent = request.user
            receiver_id = request.data['receiver_id']
            child_id = request.data['child_id']
            userChild = UserChild.objects.filter(child_id = child_id, user_id = parent.id)
            if len(userChild) == 0:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            permission = PermittedUser.objects.filter(child_id=child_id, user_id=receiver_id, parent_id=parent.id)
            if len(permission) > 0:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                permittedUser = PermittedUser.objects.create(user_id=receiver_id, child_id=child_id, parent_id=parent.id)
                permittedUser.save()
            except:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

           