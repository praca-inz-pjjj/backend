from pyclbr import Class
from urllib.request import Request
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from backbone.permisions import IsTeacher
from backbone.models import Log
from backbone.types import LogType
from teacher_panel.models import Classroom, UserClassroom
from ..serializers import ChildrenSerializer
from datetime import datetime

@api_view(['POST'])
@transaction.atomic
@permission_classes([IsTeacher])
def create_children(request: Request, id: int):
    children_data = request.data

    if not Classroom.objects.filter(id=id).exists():
        return Response({"error": "Klasa nie istnieje."}, status=status.HTTP_404_NOT_FOUND)

    if not UserClassroom.objects.filter(user_id=request.user.id, classroom_id=id).exists():
        return Response({"error": "Nie masz dostępu do tej klasy."}, status=status.HTTP_403_FORBIDDEN)

    if not isinstance(children_data, list):
        return Response({"error": "Niepoprawne dane."}, status=status.HTTP_400_BAD_REQUEST)

    for child_data in children_data:
        try:
            if datetime.strptime(child_data.get('birth_date', ''), "%Y-%m-%d") >= datetime.now():
                return Response({"error": "Data urodzenia nie może być w przyszłości."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Data urodzenia '{}' powinna być w formacie: RRRR-MM-DD.".format(child_data.get('birth_date', ''))}, status=status.HTTP_400_BAD_REQUEST)
    try:
        with transaction.atomic():
            serializer = ChildrenSerializer(data=children_data, many=True)
            if serializer.is_valid(raise_exception=True):
                children = serializer.save()
                Log.objects.create(
                    log_type=LogType.CREATE,
                    data={
                        "type": "Children",
                        "children_ids": [child.id for child in children],
                        "teacher_id": request.user.id
                    }
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        if "unique" in str(e):
            return Response({"error": "Podane dziecko już istnieje."}, status=status.HTTP_409_CONFLICT)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
