from urllib.request import Request
from django.http import FileResponse
from django.conf import settings
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from backbone.permisions import IsParent
from django.contrib.staticfiles.storage import staticfiles_storage

@api_view(['GET'])
@permission_classes([IsParent])
def authorization_letter(request: Request):
    file_path = staticfiles_storage.path('upowaznienie_wzor.pdf')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else:
        return Response({ "error": "File not found" }, status=404)
