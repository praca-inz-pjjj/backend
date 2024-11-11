from django.contrib import admin
from django.utils.html import format_html

from .models import *

# Register your models here.
@admin.register(UserChild)
class UserChildAdmin(admin.ModelAdmin):
    list_display = ("id", "user_link", "child_link")
    list_filter = ("user", "child")
    search_fields = ("user__email", "child__first_name", "child__last_name")
    ordering = ("id", "user", "child")

    def user_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.user.get_admin_url(), obj.user)
    user_link.short_description = "User"
    
    def child_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.child.get_admin_url(), obj.child)
    child_link.short_description = "Child"

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "child_link", "receiver_link", "teacher_link", "decision", "date")
    list_filter = ("child", "receiver", "teacher", "decision", "date")
    search_fields = ("child__first_name", "child__last_name", "receiver__email", "teacher__email", "date")
    ordering = ("id", "child", "receiver", "teacher", "decision", "date")
    
    def child_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.child.get_admin_url(), obj.child)
    child_link.short_description = "Child"

    def receiver_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.receiver.get_admin_url(), obj.receiver)
    receiver_link.short_description = "Receiver"
    
    def teacher_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.teacher.get_admin_url(), obj.teacher)
    teacher_link.short_description = "Teacher"

@admin.register(PermittedUser)
class PermittedUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user_link", "child_link", "parent_link", "date", "signature_delivered")
    list_filter = ("user", "child", "parent", "date", "signature_delivered")
    search_fields = ("user__email", "child__first_name", "child__last_name", "parent__email", "date")
    ordering = ("id", "user", "child", "parent", "date", "signature_delivered")

    def user_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.user.get_admin_url(), obj.user)
    user_link.short_description = "User"
    
    def child_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.child.get_admin_url(), obj.child)
    child_link.short_description = "Child"

    def parent_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.parent.get_admin_url(), obj.parent)
    parent_link.short_description = "Parent"

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "permitteduser_link", "parent_link", "state", "start_date", "end_date")
    list_filter = ("permitteduser", "parent", "state", "start_date", "end_date")
    search_fields = ("permitteduser__user__email", "parent__email", "state", "start_date", "end_date")
    ordering = ("id", "permitteduser", "parent", "state", "start_date", "end_date")

    def permitteduser_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.permitteduser.get_admin_url(), obj.permitteduser)
    permitteduser_link.short_description = "PermittedUser"

    def parent_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.parent.get_admin_url(), obj.parent)
    parent_link.short_description = "Parent"
    