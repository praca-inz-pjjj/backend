from re import I
from django.urls import path
from . import views
from .views import ObtainParentTokenPairView
from .other_views.child_receivers import ChildReceiversView
from .other_views.parent_data import ParentDataView
from .other_views.child_details import get_child_details

urlpatterns = [
    path("", ParentDataView.as_view()),
    path("token", ObtainParentTokenPairView.as_view(), name="token_obtain_pair"),
    path("permissions", views.get_permissions, name="get_permissions"),
    path("generate/<int:id>", views.generate_QR_code, name="generate_QR_code"),
    path("child/<int:id>", get_child_details, name="get_child_details"),
    path("child/<int:id>/receivers", ChildReceiversView.as_view()),
    path("child/<int:id>/permitted_users", views.get_permitted_users_for_child, name="get_permitted_users_for_child"),
    path("change-password", views.change_password, name='change-password')
]