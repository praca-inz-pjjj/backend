from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backbone.models import Log
from backbone.types import LogType
from parent_panel.serializers import HistorySerializer
from parent_panel.models import History, UserChild
from backbone.permisions import IsParent

class ParentHistoryDataView(APIView):
    permission_classes = (IsAuthenticated, IsParent, )

    def get(self, request: Request):
        parent_id = request.user.id
        parent_children_ids = UserChild.objects.filter(user_id=parent_id).values_list('child_id', flat=True)
        
        history = History.objects.filter(child_id__in=parent_children_ids)
        history_serializer = HistorySerializer(history, many=True)

        Log.objects.create(log_type=LogType.HISTORY, data={"fetcher_id": request.user.id})

        return Response({
            "history": history_serializer.data,
        })