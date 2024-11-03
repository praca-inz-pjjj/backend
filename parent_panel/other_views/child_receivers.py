from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from backbone.permisions import IsParent
from backbone.models import CustomUser
from parent_panel.other_views.commons import NO_ACCESS_TO_CHILD_RESPONSE_MESSAGE, USER_ALREADY_PERMITTED_MESSAGE
from .validators.child_validator import ChildValidator
from ..serializers import PermittedUserSerializer
from ..models import Children, PermittedUser



class ChildReceiversView(APIView):
    permission_classes = (IsParent,)

    # get all child's permitted users (parents included)
    def get(self, request: Request, child_id: int):
        parent: CustomUser = request.user
        child: Children = get_object_or_404(Children, id=child_id)

        if not ChildValidator.is_parent_of_child(parent, child):
            return Response({"message": NO_ACCESS_TO_CHILD_RESPONSE_MESSAGE}, status.HTTP_403_FORBIDDEN)

        child_permitted_users = PermittedUser.objects.filter(child=child)
        serializer = PermittedUserSerializer(child_permitted_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Permit user to child
    def post(self, request: Request, child_id: int):
        try:
            parent: CustomUser = request.user
            permitted_user_id: int = request.data['receiver_id']
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)

        child: Children = get_object_or_404(Children, id=child_id)
        permitted_user = get_object_or_404(CustomUser, id=permitted_user_id)

        if not ChildValidator.is_parent_of_child(parent, child):
            return Response({"message": NO_ACCESS_TO_CHILD_RESPONSE_MESSAGE}, status.HTTP_403_FORBIDDEN)
        
        if not ChildValidator.is_receiver_of_child(permitted_user, child):
            return Response({"message": USER_ALREADY_PERMITTED_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)

        permitted_user_entry = PermittedUser.objects.create(child=child, user=permitted_user)
        serializer = PermittedUserSerializer(permitted_user_entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # Revoke permission to child
    def delete(self, request: Request, child_id: int):
        try:
            parent: CustomUser = request.user
            permitted_user_id: int = request.data['receiver_id']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        child: Children = get_object_or_404(Children, id=child_id)
        permitted_user = get_object_or_404(CustomUser, id=permitted_user_id)

        if not ChildValidator.is_parent_of_child(parent, child):
            return Response({"message": NO_ACCESS_TO_CHILD_RESPONSE_MESSAGE}, status.HTTP_403_FORBIDDEN)

        permitted_user_entry = PermittedUser.objects.filter(child=child, user=permitted_user).first()
        if not permitted_user_entry:
            return Response({"message": "User is not permitted for this child."}, status=status.HTTP_404_NOT_FOUND)

        permitted_user_entry.delete()
        return Response({"message": "User removed from permitted list successfully."}, status=status.HTTP_204_NO_CONTENT)
