from backbone.models import CustomUser
from backbone.serializers import CustomUserSerializer
from parent_panel.models import UserChildren
from parent_panel.serializers import PartialUserChildrenSerializer
from teacher_panel.models import Children
from teacher_panel.serializers import ChildrenSerializer
from rest_framework.response import Response
from rest_framework import status



def get_child_parents(request, id):
    child = Children.objects.get(id=id)
    childParents = CustomUser.objects.filter(parent_perm = 2)
    allParents = CustomUser.objects.filter(userchildren__child_id = id)

    childSerializer = ChildrenSerializer(child)
    childParentsSerializer = CustomUserSerializer(childParents, many = True)
    ParentsSerializer = CustomUserSerializer(allParents, many = True)
    return Response({'parents': childParentsSerializer.data,
                        'all_parents': ParentsSerializer.data,
                        'child': childSerializer.data})

def delete_child_parents(request, id):
    try:
        id_parent = request.data.get('id')
        item = UserChildren.objects.get(child = id, user = id_parent)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

def post_child_parents(request, id):
    try:
        id_parent = request.data.get('id')
        serializer = PartialUserChildrenSerializer(data = {'child': id, 'user': id_parent})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)