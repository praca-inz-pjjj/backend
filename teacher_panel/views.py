from datetime import datetime
from django import shortcuts
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from backbone.models import CustomUser, Log
from backbone.types import LogType
from parent_panel.models import Permission, PermittedUser
from teacher_panel.other_views.validators.child_validator import ChildValidator
from teacher_panel.other_views.common_error_messages import NOT_CHILD_TEACHER_MESSAGE, NOT_CLASSROOM_TEACHER_MESSAGE
from teacher_panel.other_views.validators.classroom_validator import ClassroomValidator
from .serializers import ClassroomSerializer, ChildrenSerializer
from .models import *
from backbone.permisions import IsTeacher, IsIssuer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
#TODO przy logowaniu updateować last_login from django.contrib.auth.models import update_last_login

    
# Teacher home page data - first_name and last_name of teacher, classes he is teaching
@api_view(['GET'])
@permission_classes([IsTeacher])
def teacher_data(request):
    user_classes = UserClassroom.objects.filter(user_id=request.user.id)
    classes = [
        {
            'id': class_obj.classroom_id,
            'name': Classroom.objects.get(id=class_obj.classroom_id).name,
            'size': Child.objects.filter(classroom_id=class_obj.classroom_id).count()
        } for class_obj in user_classes
    ]
    teacher = CustomUser.objects.get(id=request.user.id)
    name = teacher.get_full_name()
    return Response({
        "name": name,
        "classes": classes
    })

@api_view(['GET'])
@permission_classes([IsTeacher])
def class_data(request: Request, id: int) -> Response:
    teacher = CustomUser.objects.get(id=request.user.id)
    classroom = shortcuts.get_object_or_404(Classroom,id=id)
    if not ClassroomValidator.is_teacher_of_classroom(teacher, classroom):
        return Response({"error": NOT_CLASSROOM_TEACHER_MESSAGE}, status=status.HTTP_403_FORBIDDEN)

    children = [
        {
            'id': child.id,
            'name': child.first_name,
            'surname': child.last_name,
            'birth_date': child.birth_date,
        } for child in Child.objects.filter(classroom_id=id)
    ]
    return Response({
        "id": id,
        "children": children,
        "class_name": classroom.name,
    })

           
@api_view(['POST'])
@permission_classes([IsTeacher])
def create_classroom(request):
    if request.method == 'POST':
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            classroom = serializer.save()
            # Przypisanie klasy do nauczyciela
            UserClassroom.objects.create(user=request.user, classroom=classroom)
            Log.objects.create(log_type=LogType.CREATE, data={"type" : "Classroom", "classroom_id" : classroom.id, "teacher_id" : request.user.id})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsTeacher])
def create_child(request, id):
    if datetime.strptime(request.data['birth_date'], "%Y-%m-%d") >= datetime.now():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = ChildrenSerializer(data=request.data)
    if serializer.is_valid():
        child = serializer.save()
        Log.objects.create(log_type=LogType.CREATE, data={"type" : "Child", "child_id" : child.id, "teacher_id" : request.user.id})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsIssuer])
def check_receipt(request):
    if request.method == 'GET':
        try:
            id = request.GET.get('id')
            permission = Permission.objects.get(qr_code = id)
            is_two_factor = False if permission.two_factor_code == None else True
            print(is_two_factor)
            return Response({'id': id, 'is_two_factor': is_two_factor})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
@permission_classes([IsIssuer])
def check_two_factor_code(request):
    if request.method == 'GET':
        try:
            id = request.GET.get('id')
            two_factor_code = request.GET.get('twofactor')
            print(two_factor_code)
            permission = Permission.objects.get(qr_code = id)
            correct = True if str(permission.two_factor_code) == two_factor_code else False
            print(correct)
            print(two_factor_code + " " + str(permission.two_factor_code) + " " + str(correct))
            return Response({'id': id, 'correct': correct})
        except:
            return Response(data={'correct': False})

@api_view(['PATCH'])
@permission_classes([IsTeacher])
def update_receiver_signature(request: Request, child_id: int, receiver_id: int) -> Response:
    try:
        teacher: CustomUser = request.user
        value: bool = request.data['value']

        child: Child = get_object_or_404(Child, id=child_id)

        if not ChildValidator.is_teacher_of_child(teacher, child):
            return Response({"message": NOT_CHILD_TEACHER_MESSAGE}, status.HTTP_403_FORBIDDEN)
        
        receiver: PermittedUser = get_object_or_404(PermittedUser, user_id=receiver_id, child_id=child_id)
        receiver.signature_delivered = value
        receiver.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ObtainTeacherTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if(user.teacher_perm < 1):
            raise ValidationError('Podany użytkownik nie jest nauczycielem')
        Log.objects.create(log_type=LogType.LOGIN, data={"panel": "teacher", "email": user.email})
        return token
    
class ObtainTeacherTokenPairView(TokenObtainPairView):
    serializer_class = ObtainTeacherTokenPairSerializer