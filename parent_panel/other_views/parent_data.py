import json
from django.conf import settings
from django.utils import timezone
from zoneinfo import ZoneInfo
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from backbone.models import CustomUser, Log
from backbone.types import LogType
from parent_panel.serializers import HistorySerializer, ParentChildrenSerializer
from parent_panel.models import History, UserChild
from backbone.permisions import IsParent
from teacher_panel.models import Child

class ParentDataView(APIView):
    permission_classes = (IsAuthenticated, IsParent, )

    def get(self, request: Request):
        parent_children_ids = UserChild.objects.filter(user_id=request.user.id).values_list('child_id', flat=True)
        children = Child.objects.filter(id__in=parent_children_ids)
        children_serializer = ParentChildrenSerializer(children, many=True)

        parent = get_object_or_404(CustomUser, id=request.user.id)
        name = parent.get_full_name()

        history = History.objects.filter(child_id__in=parent_children_ids)[:3]
        history_serializer = HistorySerializer(history, many=True)

        Log.objects.create(log_type=LogType.HISTORY, data={"children_ids" : list(parent_children_ids), "parent_id" : parent.id})

        return Response({
            "parent_name": name,
            "children": children_serializer.data,
            "history": history_serializer.data,
        })
