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
    path("child/<int:child_id>", get_child_details, name="get_child_details"),
    path("child/<int:child_id>/receivers", ChildReceiversView.as_view()),
    path("change-password", views.change_password, name='change-password')
]