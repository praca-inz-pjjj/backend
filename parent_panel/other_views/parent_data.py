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
from parent_panel.models import History, PermittedUser, UserChild
from backbone.permisions import IsParent
from teacher_panel.models import Child

class ParentDataView(APIView):
    permission_classes = (IsAuthenticated, IsParent, )

    def get(self, request: Request):
        # Fetch all children IDs associated with the authenticated parent
        parent_children_ids = UserChild.objects.filter(user_id=request.user.id).values_list('child_id', flat=True)
        
        # Fetch children instances using these IDs
        children = Child.objects.filter(id__in=parent_children_ids)
        
        # Serialize the children data
        children_serializer = ParentChildrenSerializer(children, many=True)

        # Fetch all permitted users associated with any of the parent's children
        receivers = PermittedUser.objects.filter(child_id__in=parent_children_ids)

        receivers_data = [
            {
                "receiver_id": receiver.user_id,
                "receiver_name": receiver.user.get_full_name(),
                "child": receiver.child_id,
                "child_name": get_object_or_404(Child.objects, id=receiver.child.id).get_full_name(),
                "parent_name": receiver.parent.get_full_name(),
                "date": timezone.localtime(receiver.date, ZoneInfo(settings.TIME_ZONE)).strftime("%Y-%m-%d"),
                "signature": receiver.signature_delivered,
                "is_parent": UserChild.objects.filter(user=receiver.user, child_id__in=parent_children_ids).exists(),
            } for receiver in receivers
        ]

        # Get the parent's full name
        parent = get_object_or_404(CustomUser, id=request.user.id)
        name = parent.get_full_name()

        # Fetch all history data
        history = History.objects.filter(child_id__in=parent_children_ids)
        history_serializer = HistorySerializer(history, many=True)

        Log.objects.create(log_type=LogType.HISTORY, data={"children_ids" : list(parent_children_ids), "parent_id" : parent.id})

        return Response({
            "parent_name": name,
            "children": children_serializer.data,
            "history": history_serializer.data,
            "receivers": receivers_data,
        })
