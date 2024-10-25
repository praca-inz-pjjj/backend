from backbone.models import CustomUser
from parent_panel.models import Children, PermittedUser, UserChildren

class ChildValidator:
    @staticmethod
    def is_parent_of_child(parent: CustomUser, child: Children) -> bool:
        return UserChildren.objects.filter(user=parent, child=child).exists()

    @staticmethod
    def is_receiver_of_child(permitted_user: CustomUser, child: Children) -> bool:
        return PermittedUser.objects.filter(child=child, user=permitted_user).exists()
