from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backbone.models import CustomUser, Log
from backbone.types import LogType


class PasswordResetConfirmView(APIView):
    def post(self, request, uid, token):
        new_password = request.data.get("new_password")
        try:
            user = CustomUser.objects.get(pk=uid)
            token_generator = PasswordResetTokenGenerator()

            if token_generator.check_token(user, token):
                user.set_password(new_password)
                user.temp_password = None
                user.save()
                Log.objects.create(log_type=LogType.PASSWORD_RESET, data={"user_id": user.id})
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
