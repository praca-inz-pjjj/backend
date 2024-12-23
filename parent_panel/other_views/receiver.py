from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from backbone.models import CustomUser, Log
from backbone.permisions import IsParent
from backbone.types import LogType
from teacher_panel.models import Child
from ..serializers import HistorySerializer
from ..models import History


class ReceiverView(APIView):
    permission_classes = (IsParent,)

    def get(self, request: Request, receiver_id: int) -> Response:
        child_id = request.query_params.get("child", None)
        if child_id:
            history = History.objects.filter(receiver=receiver_id, child=child_id)
            Log.objects.create(
                log_type=LogType.HISTORY,
                data={ "children_id": child_id, "receiver_id": receiver_id, "fetcher_id": request.user.id, },
            )
        else:
            history = History.objects.filter(receiver=receiver_id)
            Log.objects.create(
                log_type=LogType.HISTORY,
                data={"receiver_id": receiver_id, "fetcher_id": request.user.id},
            )

        history_serializer = HistorySerializer(history, many=True)
        receiver = {
            "full_name": CustomUser.objects.get(id=receiver_id).get_full_name(),
        }
        child = (
            { "full_name": Child.objects.get(id=child_id).get_full_name() }
            if child_id else {}
        )
        return Response(
            {"history": history_serializer.data, "receiver": receiver, "child": child}
        )
