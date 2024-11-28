"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import  TokenRefreshView

from backend.use_cases.passwordResetConfirm import PasswordResetConfirmView
from backend.use_cases.resetPassword import PasswordResetRequestView

from . import views
from .use_cases.changePassword import change_password

admin.site.site_title = "SafeKid site admin"
admin.site.site_header = "SafeKid administration"

urlpatterns = [
    path('', lambda req: redirect('/health')),
    path("admin/", admin.site.urls),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("teacher/", include("teacher_panel.urls")),
    path("parent/", include("parent_panel.urls")),
    path("reset-password", PasswordResetRequestView.as_view(), name="reset_password"),
    path("password-reset-confirm/<int:uid>/<str:token>/", PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path("change-password", change_password, name='change-password'),
]