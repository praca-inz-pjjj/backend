from email.message import EmailMessage
import smtplib
import ssl
from backend.settings import DEFAULT_FROM_MAIL, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT, SENDER_NAME, WEBSITE
from rest_framework.response import Response
from rest_framework import status

def sendmail(to, subject, text):
    body = text + """
        <br>
        --<br>
        <p style="font-size:0.9em; color:gray;">
        Pozdrawiamy,<br>
        Zespół {sender_name}<br>
        <a href="https://{website}">{website}</a>
        </p>
        """.format(sender_name=SENDER_NAME, website=WEBSITE)
    
    msg = EmailMessage()
    msg.set_content(body, subtype="html")
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{DEFAULT_FROM_MAIL}>"
    msg["To"] = to

    # Połączenie i wysyłka e-maila
    try:
        # context = ssl.create_default_context() #jakiś problem z default ssl certificate
        context = ssl._create_unverified_context()
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(msg)
            return Response({"message": "Wysłano wiadomość"}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)