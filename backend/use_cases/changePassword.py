from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from backbone.models import CustomUser

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(id=request.user.id)
            user.set_password(request.data['password'])
            user.temp_password = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)