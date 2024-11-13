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

class PasswordResetRequestView(APIView):

    def post(self, request):
        email = request.data.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset_url = f"{FRONTEND_LINK}/reset-password/{user.pk}/{token}/"
            print("reset url:", reset_url)
            body = """
                <p>Oto Twój link do resetu hasła: <a href="{reset_url}">link</a></p>
                <br>
                --<br>
                <p style="font-size:0.9em; color:gray;">
                Pozdrawiamy,<br>
                Zespół {sender_name}<br>
                <a href="https://{website}">{website}</a>
                </p>
                """.format(sender_name=SENDER_NAME, website=WEBSITE, reset_url=reset_url)
            
            msg = EmailMessage()
            msg.set_content(body, subtype="html")
            msg["Subject"] = "Prośba o reset hasła"
            msg["From"] = f"{SENDER_NAME} <{DEFAULT_FROM_MAIL}>"
            msg["To"] = email

            # Połączenie i wysyłka e-maila
            try:
                # context = ssl.create_default_context() #jakiś problem z default ssl certificate
                context = ssl._create_unverified_context()
                with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                    server.starttls(context=context)
                    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                    server.send_message(msg)
                    print("E-mail został wysłany pomyślnie!")
            except Exception as e:
                print("Wystąpił błąd:", e)
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
