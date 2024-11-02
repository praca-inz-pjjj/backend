from django.conf import settings
from django.utils import timezone
from zoneinfo import ZoneInfo
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from parent_panel.models import PermittedUser, UserChildren
from backbone.permisions import IsParent
from teacher_panel.models import Children


class ParentReceiversView(APIView):
    permission_classes = (IsAuthenticated, IsParent)

    def get(self, request: Request):
        # Fetch all children IDs associated with the authenticated parent
        parent_children_ids = UserChildren.objects \
            .filter(user_id=request.user.id) \
            .values_list("child_id", flat=True) 

        # Fetch all permitted users associated with any of the parent's children
        receivers = PermittedUser.objects.filter(child_id__in=parent_children_ids)

        receivers_data = [
            {
                "receiver_id": receiver.id,
                "receiver_name": receiver.user.get_full_name(),
                "child_name": get_object_or_404(Children.objects, id=receiver.child.id).get_full_name(),
                "parent_name": receiver.parent.get_full_name(),
                "date": timezone.localtime(receiver.date, ZoneInfo(settings.TIME_ZONE)).strftime("%Y-%m-%d"),
                "signature": receiver.signature_delivered,
                "is_parent": UserChildren.objects.filter(user=receiver.user, child_id__in=parent_children_ids).exists(),
            } for receiver in receivers
        ]

        return Response(receivers_data)
