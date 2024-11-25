from email import message
from http.client import BAD_REQUEST
import json
from urllib.request import Request

from django.shortcuts import get_object_or_404
from backbone.models import CustomUser, Log
from backbone.permisions import IsParent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backbone.types import LogType
from parent_panel.models import PermittedUser
from parent_panel.other_views.commons import EMAIL_IS_ALREADY_TAKEN_MESSAGE, NO_ACCESS_TO_CHILD_RESPONSE_MESSAGE, PHONE_IS_ALREADY_TAKEN_MESSAGE
from parent_panel.other_views.validators.child_validator import ChildValidator
from parent_panel.other_views.validators.user_validator import UserValidator
from teacher_panel.models import Child

class CreateReceiver(APIView):
    permission_classes = (IsParent, )
    def post(self, request: Request, child_id: int):
        parent: CustomUser = request.user
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            second_name = data.get('second_name')
            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        child: Child = get_object_or_404(Child, id=child_id)
        if not ChildValidator.is_parent_of_child(parent, child):
            return Response({"message": NO_ACCESS_TO_CHILD_RESPONSE_MESSAGE}, status.HTTP_403_FORBIDDEN)

        if UserValidator.is_email_taken(email):
            return Response({"message": EMAIL_IS_ALREADY_TAKEN_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)
        
        if UserValidator.is_phone_taken(phone):
            return Response({"message": PHONE_IS_ALREADY_TAKEN_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser(first_name=first_name,
                last_name=second_name,
                email=email,
                phone_number=phone,
                is_superuser=False,
                is_active=True,
                teacher_perm = 0,
                parent_perm = 1,
                temp_password=password)
            user.set_password(password)
            user.save()
            Log.objects.create(log_type=LogType.CREATE, data={"type" : "User", "user_id" : user.id, "creator_id" : parent.id})

            permitted_user = PermittedUser(
                user = user,
                child = child,
                parent = parent
            )
            permitted_user.save()
            Log.objects.create(log_type=LogType.CREATE, data={"type" : "Permitted User", "permitted_user_id" : permitted_user.id, "parent_id" : parent.id})

            return Response({
                'first_name': first_name,
                'second_name': second_name,
                'email': email,
                'phone': phone,
                'password': password
            }, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        