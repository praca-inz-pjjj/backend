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
from parent_panel.models import PermittedUser, UserChildren
from backbone.permisions import IsParent
from teacher_panel.models import Children

class ParentChildrenView(APIView):
    permission_classes = (IsAuthenticated, IsParent, )

    def get(self, request: Request):
        parent_children_ids = UserChildren.objects.filter(user_id=request.user.id).values_list('child_id', flat=True)
        
        children = Children.objects.filter(id__in=parent_children_ids)        
        children_serializer = ParentChildrenSerializer(children, many=True)

        return Response(children_serializer.data)
