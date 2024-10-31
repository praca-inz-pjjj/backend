import json

from django.http import HttpResponse
from backbone.models import CustomUser
from backbone.permisions import IsTeacher
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from parent_panel.models import UserChildren
from teacher_panel.models import Children
from csv import writer


class DownloadParentList(APIView):
    permission_classes = [IsTeacher]

    def get(self, request, id):
        try:
            class_id = id
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            children_ids = Children.objects.filter(classroom = class_id).values_list('id', flat=True)
            user_ids = UserChildren.objects.filter(child__in = children_ids).values_list('user', flat=True).distinct()
            users = CustomUser.objects.filter(id__in = user_ids)

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="users_class_{class_id}.csv"'
            response.write('\ufeff'.encode('utf-8'))
            csv_writer = writer(response, delimiter=';')

            csv_writer.writerow(['Imię', 'Nazwisko', 'Tymczasowe Hasło'])

            for user in users:
                csv_writer.writerow([user.first_name, user.last_name, user.temp_password])
            
            return response
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

