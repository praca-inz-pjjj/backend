from django.urls import path
from . import views
from rest_framework_simplejwt.views import  TokenRefreshView, TokenObtainPairView
from .views import ObtainParentTokenPairView

urlpatterns = [
    path("", views.send_some_data),
    path("token", ObtainParentTokenPairView.as_view(), name="token_obtain_pair"),
    path("permissions", views.get_permissions, name="get_permissions"),
    path("generate/<int:id>", views.generate_QR_code, name="generate_QR_code")
]