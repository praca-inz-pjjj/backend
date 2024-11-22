from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from backbone.models import CustomUser
from backend.settings import FRONTEND_LINK
from backend.utils.sendmail import sendmail

class PasswordResetRequestView(APIView):

    def post(self, request):
        email = request.data.get("email")
        try:
            if not email:
                return Response({"message": "Nie podano adresu email."}, status=status.HTTP_400_BAD_REQUEST)
            if not CustomUser.objects.filter(email=email).exists():
                return Response({"message": "Użytkownik o podanym adresie email nie istnieje."}, status=status.HTTP_404_NOT_FOUND)
            user = CustomUser.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset_url = f"{FRONTEND_LINK}/reset-password/{user.pk}/{token}/"
            print("reset url:", reset_url)
            
            subject = "Resetowanie hasła"
            text = f"""
            <p>Cześć, {user.first_name}!</p>
            <p>Otrzymaliśmy prośbę o zresetowanie Twojego hasła. Jeśli ta prośba nie pochodzi od Ciebie, zignoruj to powiadomienie. W przeciwnym razie możesz zresetować hasło za pomocą tego linku:</p>
            <p style="text-align: center;">
                <a href="{reset_url}" 
                   style="background-color: #007bff; color: white; padding: 15px 30px; font-size: 16px; text-decoration: none; border-radius: 5px; display: inline-block;">
                   Resetuj hasło
                </a>
            </p>
            """
            return sendmail(email, subject, text)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
