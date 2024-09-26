from secrets import randbelow
from zoneinfo import ZoneInfo

from django.shortcuts import render
from django.http import HttpRequest
from django.utils import timezone
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from backbone.permisions import IsReceiver
from backbone.models import CustomUser

from .models import *

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_some_data(request: HttpRequest):
   
    return Response({
        "data": "Hello from parent api",
    })

# TODO: Change get_permissions to return every info we need in mobile homepage for parent and receiver
# Get all Permissions of the Receiver
@api_view(['GET'])
@permission_classes([IsReceiver])
def get_permissions(request):
    user = CustomUser.objects.get(id=request.user.id)
    permissions = []
    objects = Permission.objects.filter(permitteduser__user=user)
    for obj in objects:
        if (obj.end_date < timezone.now()):
            obj.state = PermissionState.CLOSED
            obj.save()
        if obj.state != PermissionState.CLOSED:
            permissions.append({
                "id": obj.id, "parent": obj.parent.get_full_name(), "state": obj.state,
                "start_date": timezone.localtime(obj.start_date, ZoneInfo(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S"),
                "end_date": timezone.localtime(obj.end_date, ZoneInfo(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")
                })
    return Response({
        "permissions": permissions
    })

# Create QR Code for Permission of a given ID
@api_view(['POST'])
@permission_classes([IsReceiver])
def generate_QR_code(request, id):
    if request.method == 'POST':
        receiver = CustomUser.objects.get(id=request.user.id)
        permission = Permission.objects.get(id=id)
        permitted_user = PermittedUser.objects.get(id=permission.permitteduser.id)
        if (permission.state == PermissionState.CLOSED):
            return Response({"data": "This permission is already closed"}, status.HTTP_418_IM_A_TEAPOT)
        if (permitted_user.user != receiver):
            return Response({"data": "You don't have access to this permission, how did you get here?"}, status.HTTP_403_FORBIDDEN)
        if (permission.start_date > timezone.now()):
            return Response({"data": "Too early to generate QR Code"}, status.HTTP_412_PRECONDITION_FAILED)
        if (permission.end_date < timezone.now()):
            permission.state = PermissionState.CLOSED
            permission.save()
            return Response({"data": "This permission has expired"}, status.HTTP_412_PRECONDITION_FAILED)
        generated_qr_code = randbelow(90000000) + 10000000
        print("Generated QR Code: " + str(generated_qr_code))
        permission.qr_code = generated_qr_code
        if (permission.state == PermissionState.SLEEP or permission.state == PermissionState.NOTIFY):
            permission.state = PermissionState.ACTIVE
        permission.save()
        return Response({"qr_code": generated_qr_code}, status=status.HTTP_201_CREATED)
