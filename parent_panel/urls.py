from django.urls import path

from parent_panel.other_views.create_receiver import CreateReceiver

from . import views
from .views import ObtainParentTokenPairView
from .other_views.child_receivers import ChildReceiversView
from .other_views.parent_data import ParentDataView
from .other_views.child_details import get_child_details
from .other_views.parent_receivers import ParentReceiversView
from .other_views.receiver import ReceiverView
from parent_panel.other_views.parent_children import ParentChildrenView
from .other_views.receiver_signature import ReceiverSignatureView
from .other_views.history import ParentHistoryDataView

urlpatterns = [
    path("", ParentDataView.as_view()),
    path("token", ObtainParentTokenPairView.as_view(), name="token_obtain_pair"),
    path("permissions", views.get_permissions, name="get_permissions"),
    path("generate/<int:id>", views.generate_QR_code, name="generate_QR_code"),
    path("child/all", views.get_all_children, name="get_all_children"),
    path("child/<int:id>", get_child_details, name="get_child_details"),
    path("child/<int:child_id>/receivers", ChildReceiversView.as_view()),
    path("child/<int:id>/permitted-users", views.get_permitted_users_for_child, name="get_permitted_users_for_child"),
    path("child/<int:id>/create-permission", views.create_permission, name="create_permission"),
    path("permission/<int:perm_id>", views.delete_permission, name="delete_permission"),
    path("receivers", ParentReceiversView.as_view(), name="get_parent_receivers"),
    path("children", ParentChildrenView.as_view(), name="get_parent_children"),
    path("child/<int:child_id>/create-receiver", CreateReceiver.as_view(), name="create_receiver"),
    path("receiver/<int:receiver_id>/signature", ReceiverSignatureView.as_view(), name="receiver_signature"),
    path("receiver/<int:receiver_id>", ReceiverView.as_view(), name="get_receiver_details"),
    path("history", ParentHistoryDataView.as_view(), name="get_parent_history"),
]