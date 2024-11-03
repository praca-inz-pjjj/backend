from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from backbone.permisions import IsParent
from ..serializers import PermittedUserSerializer
from ..models import PermittedUser

class ReceiversView(APIView):
    permission_classes = (IsParent,)

    def get(self, _request: Request):
        permitted_users = PermittedUser.objects.all()
        serializer = PermittedUserSerializer(permitted_users, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
