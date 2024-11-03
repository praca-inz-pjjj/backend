from django.conf import settings
from django.utils import timezone
from zoneinfo import ZoneInfo
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from backbone.models import CustomUser
from parent_panel.serializers import ParentChildrenSerializer
from parent_panel.models import PermittedUser, UserChild
from backbone.permisions import IsParent
from teacher_panel.models import Child

class ParentDataView(APIView):
    permission_classes = (IsAuthenticated, IsParent, )

    def get(self, request: Request):
        # Fetch all children IDs associated with the authenticated parent
        user_children_ids = UserChild.objects.filter(user_id=request.user.id).values_list('child_id', flat=True)
        
        # Fetch children instances using these IDs
        children = Child.objects.filter(id__in=user_children_ids)
        
        # Serialize the children data
        children_serializer = ParentChildrenSerializer(children, many=True)

        # Fetch all permitted users associated with any of the parent's children
        permitted_users = PermittedUser.objects.filter(child_id__in=user_children_ids)

        permitted_users_data = []
        for permitted_user in permitted_users:
            user_data = {
                "user_id": permitted_user.id,
                "user_name": permitted_user.user.get_full_name(),
                "child_name": Child.objects.filter(id=permitted_user.child.id).first().get_full_name(),
                "parent_name": permitted_user.parent.get_full_name(),
                "date": timezone.localtime(permitted_user.date, ZoneInfo(settings.TIME_ZONE)).strftime("%Y-%m-%d"),
                "signature": permitted_user.signature_delivered,
                "is_parent": UserChild.objects.filter(user=permitted_user.user, child_id__in=user_children_ids).exists(),
            }
            permitted_users_data.append(user_data)

        # Get the parent's full name
        parent = get_object_or_404(CustomUser, id=request.user.id)
        name = parent.get_full_name()

        return Response({
            "parent_id": parent.id,
            "parent_name": name,
            "children": children_serializer.data,
            "permitted_users": permitted_users_data,
        })
