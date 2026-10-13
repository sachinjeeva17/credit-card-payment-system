from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "date_joined",
        "last_login",
        "is_active",
        "is_staff",
    ]
    list_display_links = ["id", "username"]

    list_filter = [
        "is_active",
        "is_staff",
        "date_joined",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]

    ordering = ["-date_joined"]

from django.contrib.admin.models import LogEntry


@admin.register(LogEntry)
class AdminLogAdmin(admin.ModelAdmin):

    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_repr",
        "action_flag",
    ]

    list_filter = [
        "action_time",
        "action_flag",
    ]

    search_fields = [
        "user__username",
        "object_repr",
    ]

    readonly_fields = [
        "action_time",
        "user",
        "content_type",
        "object_id",
        "object_repr",
        "action_flag",
        "change_message",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False