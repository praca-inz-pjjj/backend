from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from backbone.models import CustomUser
from backbone.permisions import IsParent
from parent_panel.models import PermittedUser
from parent_panel.other_views.common_error_messages import NO_ACCESS_TO_CHILD_RESPONSE_MESSAGE
from parent_panel.other_views.validators.child_validator import ChildValidator
from teacher_panel.models import Child


class ReceiverSignatureView(APIView):
    permission_classes = (IsParent, IsAuthenticated)

    def post(self, request: Request, receiver_id: int):
        try:
            parent: CustomUser = request.user
            child_id: int = request.data['child_id']

            child: Child = get_object_or_404(Child, id=child_id)

            if not ChildValidator.is_parent_of_child(parent, child):
                return Response({"message": NO_ACCESS_TO_CHILD_RESPONSE_MESSAGE}, status.HTTP_403_FORBIDDEN)
            
            receiver: PermittedUser = get_object_or_404(PermittedUser, user_id=receiver_id, child_id=child_id)
            receiver.signature_delivered = True
            receiver.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, child_id: int):
        pass