from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from backbone.models import CustomUser
from backbone.permisions import IsParent
from backbone.types import PermissionState
from parent_panel.models import Child, UserChild, PermittedUser, Permission
from django.utils import timezone
from zoneinfo import ZoneInfo
from django.conf import settings

from parent_panel.other_views.commons import NO_ACCESS_TO_CHILD_RESPONSE_MESSAGE
from parent_panel.other_views.validators.child_validator import ChildValidator

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsParent])
def get_child_details(request: Request, id: int):
    parent = get_object_or_404(CustomUser, id=request.user.id)
    child = get_object_or_404(Child, id=id)
    
    if not ChildValidator.is_parent_of_child(parent, child):
            return Response({"message": NO_ACCESS_TO_CHILD_RESPONSE_MESSAGE}, status.HTTP_403_FORBIDDEN)

    permitted_users_data = []
    permitted_users = PermittedUser.objects.filter(child=child)
    for permitted_user in permitted_users:
        user_data = {
            "user_id": permitted_user.user.id,
            "user_name": permitted_user.user.get_full_name(),
            "parent_name": permitted_user.parent.get_full_name(),
            "date": timezone.localtime(permitted_user.date, ZoneInfo(settings.TIME_ZONE)).strftime("%Y-%m-%d"),
            "signature": permitted_user.signature_delivered,
            "is_parent": UserChild.objects.filter(user=permitted_user.user, child=child).exists(),
        }
        permitted_users_data.append(user_data)

    permissions_data = []
    permitted_users_ids = permitted_users.values_list('id', flat=True)
    permissions = Permission.objects.filter(permitteduser__in=permitted_users_ids)
    for permission in permissions:
        if (permission.end_date < timezone.now() and permission.state != PermissionState.PERMANENT and permission.state != PermissionState.CLOSED):
            permission.state = PermissionState.CLOSED
            permission.save()
        if permission.state in (PermissionState.CLOSED, PermissionState.PERMANENT):
            continue
        permission_data = {
            "permission_id": permission.id,
            "user_name": permission.permitteduser.user.get_full_name(),
            "state": permission.state,
            "start_date": timezone.localtime(permission.start_date, ZoneInfo(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": timezone.localtime(permission.end_date, ZoneInfo(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S"),
        }
        permissions_data.append(permission_data)

    return Response({
        "child_id": child.id, 
        "child_name": child.get_full_name(),
        "permitted_users": permitted_users_data,
        "permissions": permissions_data
    })
