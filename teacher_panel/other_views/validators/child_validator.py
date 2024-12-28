from backbone.models import CustomUser
from parent_panel.models import Child
from teacher_panel.models import UserClassroom

class ChildValidator:
    @staticmethod
    def is_teacher_of_child(teacher: CustomUser, child: Child) -> bool:
        return UserClassroom.objects.filter(user=teacher, classroom=child.classroom).exists()