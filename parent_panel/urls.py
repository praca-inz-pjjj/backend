from django.urls import path

from parent_panel.other_views.create_receiver import CreateReceiver

from . import views
from .views import ObtainParentTokenPairView
from .other_views.child_receivers import ChildReceiversView
from .other_views.parent_data import ParentDataView
from .other_views.child_details import get_child_details
from .other_views.parent_receivers import ParentReceiversView
from parent_panel.other_views.parent_children import ParentChildrenView

urlpatterns = [
    path("", ParentDataView.as_view()),
    path("token", ObtainParentTokenPairView.as_view(), name="token_obtain_pair"),
    path("permissions", views.get_permissions, name="get_permissions"),
    path("generate/<int:id>", views.generate_QR_code, name="generate_QR_code"),
    path("child/<int:child_id>", get_child_details, name="get_child_details"),
    path("child/<int:child_id>/receivers", ChildReceiversView.as_view()),
    path("change-password", views.change_password, name='change-password'),
    path("receivers", ParentReceiversView.as_view(), name="get_parent_receivers"),
    path("children", ParentChildrenView.as_view(), name="get_parent_children"),
    path("child/<int:child_id>/create-receiver", CreateReceiver.as_view(), name="create_receiver")
]