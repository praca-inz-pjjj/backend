from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from backbone import serializers
from backbone.permisions import IsParent
from backbone.models import CustomUser
from .validators.child_validator import ChildValidator
from ..serializers import PermittedUserSerializer
from ..models import Child, PermittedUser

class ReceiversView(APIView):
    permission_classes = (IsParent,)

    def get(self, _request: Request):
        permitted_users = PermittedUser.objects.all()
        serializer = PermittedUserSerializer(permitted_users, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request: Request):
        # TODO
