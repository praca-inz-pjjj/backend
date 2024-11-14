from email.message import EmailMessage
import smtplib
import ssl
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.urls import reverse

from backbone.models import CustomUser
from backend.settings import DEFAULT_FROM_MAIL, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT, FRONTEND_LINK, SENDER_NAME, WEBSITE
from backend.utils.sendmail import sendmail

class PasswordResetRequestView(APIView):

    def post(self, request):
        email = request.data.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset_url = f"{FRONTEND_LINK}/reset-password/{user.pk}/{token}/"
            print("reset url:", reset_url)
            text = f"<p>Oto Twój link do resetu hasła: <a href=\"{reset_url}\">link</a></p>"
            subject = "Prośba o reset hasła"
            return sendmail(email, subject, text)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
