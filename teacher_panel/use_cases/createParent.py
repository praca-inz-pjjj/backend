import json
from backbone.models import CustomUser
from backbone.permisions import IsTeacher
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CreateParent(APIView):
    permission_classes = [IsTeacher]
    def post(self, request):
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            second_name = data.get('second_name')
            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser(first_name=first_name,
                last_name=second_name,
                email=email,
                phone_number=phone,
                is_superuser=False,
                is_active=True,
                teacher_perm = 0,
                parent_perm = 2,
                temp_password=password)
            user.set_password(password)
            user.save()
            return Response({
                'first_name': first_name,
                'second_name': second_name,
                'email': email,
                'phone': phone,
                'password': password
            }, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        