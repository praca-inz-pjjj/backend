from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backbone.models import Log
from backbone.types import LogType
from parent_panel.serializers import HistorySerializer
from parent_panel.models import History, UserChild
from backbone.permisions import IsParent, IsReceiver

class ParentHistoryDataView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request):
        is_receiver = IsReceiver().has_permission(request, self)
        is_parent = IsParent().has_permission(request, self)

        if not is_receiver:
            return Response({"error": "You are not a receiver"}, status=403)
        
        history = None
        history_serializer = None

        if is_receiver and not is_parent:
            history = History.objects.filter(receiver_id=request.user.id)
            history_serializer = HistorySerializer(history, many=True)
        else:
            parent_id = request.user.id
            parent_children_ids = UserChild.objects.filter(user_id=parent_id).values_list('child_id', flat=True)
            
            history = History.objects.filter(child_id__in=parent_children_ids)
            history_serializer = HistorySerializer(history, many=True)

        Log.objects.create(log_type=LogType.HISTORY, data={"fetcher_id": request.user.id})

        return Response({
            "history": history_serializer.data,
        })