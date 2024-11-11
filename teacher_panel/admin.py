from django.contrib import admin
from django.utils.html import format_html

from parent_panel.models import UserChild

from .models import *

# Register your models here.

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "children_link")
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    def children_link(self, obj):
        child_count = obj.child_set.count()
        url = (
            reverse("admin:teacher_panel_child_changelist")
            + f"?classroom__id__exact={obj.id}"
        )
        return format_html('<a href="{}">{} Children</a>', url, child_count)
    children_link.short_description = "Number of Children"

@admin.register(UserClassroom)
class UserClassroomAdmin(admin.ModelAdmin):
    list_display = ("id", "user_link", "classroom_link")
    list_filter = ("user", "classroom")
    search_fields = ("user__email", "classroom__name")
    ordering = ("id", "user", "classroom")

    def user_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.user.get_admin_url(), obj.user)
    user_link.short_description = "User"

    def classroom_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.classroom.get_admin_url(), obj.classroom)
    classroom_link.short_description = "Classroom"

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ("__str__", "classroom_link", "parents_link")
    list_filter = ("first_name", "last_name", "classroom" )
    search_fields = ("first_name", "last_name", "classroom__name")
    ordering = ("classroom", "last_name", "first_name")

    def classroom_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.classroom.get_admin_url(), obj.classroom)
    classroom_link.short_description = "Classroom"

    def parents_link(self, obj):
        # Find all parent users associated with this child through the UserChild model
        user_ids = UserChild.objects.filter(child=obj).values_list("user", flat=True)
        count = len(user_ids)
        
        # Create a link to the User admin page with a filter on the list of user IDs
        url = (
            reverse("admin:backbone_customuser_changelist")  # Replace `yourapp_customuser_changelist` with your actual User model admin path
            + f"?id__in={','.join(map(str, user_ids))}"
        )

        return format_html('<a href="{}">{} Parent{}</a>', url, count, '' if count == 1 else 's')
    parents_link.short_description = "Parents"
