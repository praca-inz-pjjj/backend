from django.utils import timezone
from rest_framework.request import Request
from backbone.models import CustomUser, Log
from backbone.permisions import IsTeacher
from backbone.serializers import CustomUserSerializer, PermittedUserSerializer
from backbone.types import LogType, PermissionState
from parent_panel.models import PermittedUser, UserChild
from parent_panel.serializers import UserChildrenSerializer, PermissionSerializer
from teacher_panel.models import Child, Classroom
from teacher_panel.other_views.common_error_messages import NOT_CHILD_TEACHER_MESSAGE
from teacher_panel.other_views.validators.child_validator import ChildValidator
from teacher_panel.serializers import ChildrenSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction

class ChildParentsView(APIView):
    permission_classes = [IsTeacher]
    def get(self, request: Request, id: int):
        try:
            child = Child.objects.get(id=id)
            if not ChildValidator.is_teacher_of_child(request.user, child):
                return Response(
                    {"error": NOT_CHILD_TEACHER_MESSAGE},
                    status=status.HTTP_403_FORBIDDEN,
                )

            allParents = CustomUser.objects.filter(parent_perm=2)
            childParents = CustomUser.objects.filter(userchild__child_id=id)
            childClassroom = Classroom.objects.get(id=child.classroom_id)

            childSerializer = ChildrenSerializer(child)
            childParentsSerializer = CustomUserSerializer(childParents, many=True)
            parentsSerializer = CustomUserSerializer(allParents, many=True)

            childReceiversWithoutDeliveredSignature = PermittedUser.objects.filter(
                child=id, signature_delivered=False
            )
            receivers = CustomUser.objects.filter(
                id__in=childReceiversWithoutDeliveredSignature.values("user")
            ).exclude(id__in=childParents.values("id"))
            receiversSerializer = CustomUserSerializer(receivers, many=True)

            return Response(
                {
                    "classroom": {"id": childClassroom.id, "name": childClassroom.name},
                    "parents": childParentsSerializer.data,
                    "all_parents": parentsSerializer.data,
                    "child": childSerializer.data,
                    "receivers": receiversSerializer.data,
                }
            )
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def delete(self, request: Request, id: int):
        try:
            child = Child.objects.get(id=id)
            if not ChildValidator.is_teacher_of_child(request.user, child):
                return Response(
                    {"error": NOT_CHILD_TEACHER_MESSAGE},
                    status=status.HTTP_403_FORBIDDEN,
                )

            parent_id = request.data.get('id')
            with transaction.atomic():
                item = UserChild.objects.get(child=id, user=parent_id)
                item.delete()

                permittedUser = PermittedUser.objects.get(child=id, user=parent_id, parent=parent_id)
                permittedUser.delete()

                Log.objects.create(
                    log_type=LogType.DELETE,
                    data={
                        "type": "UserChild",
                        "child_id": id,
                        "parent_id": parent_id,
                        "teacher_id": request.user.id
                    }
                )

            return Response(status=status.HTTP_204_NO_CONTENT)

        except UserChild.DoesNotExist:
            return Response({'error': 'UserChild not found.'}, status=status.HTTP_404_NOT_FOUND)
        except PermittedUser.DoesNotExist:
            return Response({'error': 'PermittedUser not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def post(self, request: Request, id: int):
        try:
            child = Child.objects.get(id=id)
            if not ChildValidator.is_teacher_of_child(request.user, child):
                return Response(
                    {"error": NOT_CHILD_TEACHER_MESSAGE},
                    status=status.HTTP_403_FORBIDDEN,
                )
            
            parent_id = request.data.get('id')
            with transaction.atomic():
                userChildrenSerializer = UserChildrenSerializer(data={'child': id, 'user': parent_id})
                if not userChildrenSerializer.is_valid():
                    return Response({'error': userChildrenSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                userChildrenSerializer.save()

                permittedUserSerializer = PermittedUserSerializer(data={'child': id, 'parent': parent_id, 'user': parent_id})
                if not permittedUserSerializer.is_valid():
                    return Response({'error': permittedUserSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                saved_permittedUser = permittedUserSerializer.save()

                permissionSerializer = PermissionSerializer(data={
                    'permitteduser': saved_permittedUser.id,
                    'state': PermissionState.PERMANENT,
                    'parent': parent_id,
                    'end_date': timezone.now()
                })
                if not permissionSerializer.is_valid():
                    return Response({'error': permissionSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                permissionSerializer.save()

                Log.objects.create(
                    log_type=LogType.CREATE,
                    data={
                        "type": "UserChild",
                        "child_id": id,
                        "parent_id": parent_id,
                        "teacher_id": request.user.id
                    }
                )

            return Response(userChildrenSerializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

