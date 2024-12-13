import json
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from backbone.models import Log
from backbone.permisions import IsParent
from backbone.types import LogType
from ..serializers import HistorySerializer
from ..models import History

class ReceiverView(APIView):
    permission_classes = (IsParent,)

    def get(self, request: Request, receiver_id: int) -> Response:
        child_id = request.query_params.get('child')
        history = History.objects.filter(receiver=receiver_id, child=child_id)
        history_serializer = HistorySerializer(history, many=True)

        Log.objects.create(log_type=LogType.HISTORY, data={"children_id" : child_id, "receiver_id" : receiver_id, "fetcher_id": request.user.id})

        return Response({
            "history": history_serializer.data,
        })

