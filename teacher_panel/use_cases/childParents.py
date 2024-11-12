from pyclbr import Class
from django.utils import timezone
from backbone.models import CustomUser
from backbone.permisions import IsTeacher
from backbone.serializers import CustomUserSerializer, PermittedUserSerializer
from backbone.types import PermissionState
from parent_panel.models import Permission, PermittedUser, UserChild
from parent_panel.serializers import UserChildrenSerializer, PermissionSerializer
from teacher_panel.models import Child, Classroom
from teacher_panel.serializers import ChildrenSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class ChildParentsView(APIView):
    permission_classes = [IsTeacher]
    def get(self, request, id):
        try:
            child = Child.objects.get(id=id)
            allParents = CustomUser.objects.filter(parent_perm = 2)
            childParents = CustomUser.objects.filter(userchild__child_id = id)
            childClassroom = Classroom.objects.get(id = child.classroom_id)

            childSerializer = ChildrenSerializer(child)
            childParentsSerializer = CustomUserSerializer(childParents, many = True)
            parentsSerializer = CustomUserSerializer(allParents, many = True)

            print(childParentsSerializer.data)
            return Response({
                'classroom': {
                    'id': childClassroom.id,
                    'name': childClassroom.name
                },
                'parents': childParentsSerializer.data,
                'all_parents': parentsSerializer.data,
                'child': childSerializer.data
                })
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            id_parent = request.data.get('id')
            item = UserChild.objects.get(child = id, user = id_parent)
            item.delete()

            permittedUser = PermittedUser.objects.get(child = id, user = id_parent, parent = id_parent)
            permittedUser.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        try:
            id_parent = request.data.get('id')
            serializer = UserChildrenSerializer(data = {'child': id, 'user': id_parent})
            if serializer.is_valid():
                serializer.save()
                permittedUserSerializer = PermittedUserSerializer(data = {'child': id, 'parent': id_parent, 'user': id_parent})
                if permittedUserSerializer.is_valid():
                    saved_permittedUser = permittedUserSerializer.save()
                    permissionSerializer = PermissionSerializer(data = {'permitteduser': saved_permittedUser.id, 'state': PermissionState.PERMANENT, 'parent': id_parent, 'end_date': timezone.now()})
                    if permissionSerializer.is_valid():
                        permissionSerializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)