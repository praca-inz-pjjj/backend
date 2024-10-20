from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from backbone.models import CustomUser
from .serializers import ClassroomSerializer, ChildrenSerializer
from .models import *
from backbone.permisions import IsTeacher
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
#TODO przy logowaniu updateować last_login from django.contrib.auth.models import update_last_login

    
# Teacher home page data - name and surname of teacher, classes he is teaching
@api_view(['GET'])
@permission_classes([IsTeacher])
def teacher_data(request):
    classes = dict()
    user_classes = UserClassroom.objects.filter(user_id=request.user.id)
    for class_obj in user_classes:
         classes[class_obj.classroom_id] = Classroom.objects.get(id=class_obj.classroom_id).name
    teacher = CustomUser.objects.get(id=request.user.id)
    name = teacher.get_full_name()
    return Response({
        "name": name,
        "classes": classes
    })

@api_view(['GET'])
@permission_classes([IsTeacher])
def class_data(request, id):
    children = dict()
    objects = Children.objects.filter(classroom_id=id)
    for obj in objects:
        children[obj.id] = {'name': obj.name, 'surname': obj.surname}
    classroom = Classroom.objects.get(id=id)
    return Response({
        "id": id,
        "children": children,
        "class_name": classroom.name,
    })
    

# class LogoutView(APIView):
#      permission_classes = (IsTeacher,)
#      def post(self, request):
#           try:
#                refresh_token = request.data["refresh_token"]
#                token = RefreshToken(refresh_token)
#                token.blacklist()
#                return Response(status=status.HTTP_205_RESET_CONTENT)
#           except Exception as e:
#                return Response(status=status.HTTP_400_BAD_REQUEST)
           
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_classroom(request):
    if request.method == 'POST':
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            classroom = serializer.save()
            # Przypisanie klasy do nauczyciela
            UserClassroom.objects.create(user=request.user, classroom=classroom)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsTeacher])
def create_child(request, id):
    if request.method == 'POST':
        serializer = ChildrenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainTeacherTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(user.teacher_perm)
        if(user.teacher_perm != 2):
            raise ValidationError('Podany użytkownik nie jest nauczycielem')
        return token
    
class ObtainTeacherTokenPairView(TokenObtainPairView):
    serializer_class = ObtainTeacherTokenPairSerializer