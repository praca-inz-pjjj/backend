from backbone.models import CustomUser
from teacher_panel.models import Classroom, UserClassroom

class ClassroomValidator:
    @staticmethod
    def is_teacher_of_classroom(teacher: CustomUser, classroom: Classroom) -> bool:
        return UserClassroom.objects.filter(user=teacher, classroom=classroom).exists()