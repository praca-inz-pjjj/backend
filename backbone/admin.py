from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)
        field_classes = {"email": forms.EmailField}

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)
        field_classes = {"email": forms.EmailField}

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "first_name", "last_name", "teacher_perm", "parent_perm", "is_superuser")
    list_filter = ("email", "first_name", "last_name", "teacher_perm", "parent_perm", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informacje", {"fields": ("first_name", "last_name", "phone_number", "last_login", "date_joined")}),
        ("Pozwolenia", {"fields": ("teacher_perm", "parent_perm", "is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email", "teacher_perm", "parent_perm", "is_superuser")
    
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("id", "log_type", "date")
    list_filter = ("log_type", "date")
    search_fields = ("log_type", "date")
    ordering = ("id", "log_type", "date")
 
@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ("id", "consent_type", "change_date")
    list_filter = ("consent_type", "change_date")
    search_fields = ("consent_type", "change_date")
    ordering = ("id", "consent_type", "change_date")

@admin.register(UserConsent)
class UserConsentAdmin(admin.ModelAdmin):
    list_display = ("id", "user_link", "consent_link", "signing_date", "seen_changes")
    list_filter = ("user", "consent", "signing_date", "seen_changes")
    search_fields = ("user__email", "consent__id", "signing_date")
    ordering = ("id", "user", "consent", "signing_date")

    def user_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.user.get_admin_url(), obj.user)
    user_link.short_description = "User"
    
    def consent_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.consent.get_admin_url(), obj.consent)
    consent_link.short_description = "Consent"
