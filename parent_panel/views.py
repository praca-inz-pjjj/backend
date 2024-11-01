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
from backbone.permisions import IsReceiver, IsParent
from backbone.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from teacher_panel.serializers import ChildrenSerializer
from .serializers import PermissionSerializer

from .models import *

# TODO: Change get_permissions to return every info we need in mobile homepage for parent and receiver
# Get all Permissions of the Receiver
@api_view(['GET'])
@permission_classes([IsReceiver])
def get_permissions(request):
    user = CustomUser.objects.get(id=request.user.id)
    permissions = []
    objects = Permission.objects.filter(permitteduser__user=user)
    for obj in objects:
        if (obj.end_date < timezone.now() and obj.state != PermissionState.PERMANENT ):
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
        if (permission.end_date < timezone.now() and permission.state != PermissionState.PERMANENT):
            permission.state = PermissionState.CLOSED
            permission.save()
            return Response({"data": "This permission has expired"}, status.HTTP_412_PRECONDITION_FAILED)
        generated_qr_code = randbelow(90000000) + 10000000
        print("Generated QR Code: " + str(generated_qr_code))
        permission.qr_code = generated_qr_code
        if (permission.state == PermissionState.SLEEP or permission.state == PermissionState.NOTIFY):
            permission.state = PermissionState.ACTIVE
        if permission.state == PermissionState.PERMANENT:
            permission.end_date = timezone.now() + timedelta(minutes=5)
        permission.save()
        return Response({"qr_code": generated_qr_code}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsParent])
def get_permitted_users_for_child(request, id):
    if request.method == 'GET':
        parent = CustomUser.objects.get(id=request.user.id)
        child = Children.objects.get(id=id)
        is_connection = UserChildren.objects.filter(user=parent, child=child).exists()
        if not is_connection:
            return Response({"data": "You don't have access to this child, how did you get here?"}, status.HTTP_403_FORBIDDEN)
        permitted_users = PermittedUser.objects.filter(child=child)
        permitted_users_data = dict()
        for index, permitted_user in enumerate(permitted_users):
            permitted_users_data[index + 1] = {"id" : permitted_user.id,
                                               "user" : permitted_user.user.get_full_name(), 
                                               "is_parent" : UserChildren.objects.filter(user=permitted_user.user, child=child).exists()
                                       }
        return Response({
            "permitted_users" : permitted_users_data
        })

@api_view(['POST'])
@permission_classes([IsParent])
def create_permission(request):
    if request.method == 'POST':
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            permission = serializer.save()
            # Wpisanie permisji do bazy danych
            Permission.objects.create("""TODO""")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsParent])
def change_password(request):
    if request.method == 'POST':
        print(request.user.id)
        print(request.data['userId'], request.data['password'])
        try:
            user = CustomUser.objects.get(id=request.user.id)
            user.set_password(request.data['password'])
            user.temp_password = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ObtainParentTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if(user.parent_perm != 2):
            raise ValidationError('Podany użytkownik nie jest rodzicem')
        token['temp_password'] = user.temp_password
        return token
    def validate(self, attrs):
        data = super().validate(attrs)

        # Dodajemy informację do odpowiedzi, jeśli użytkownik ma tymczasowe hasło
        data['temp_password'] = self.user.temp_password
        
        return data
    
class ObtainParentTokenPairView(TokenObtainPairView):
    serializer_class = ObtainParentTokenPairSerializer