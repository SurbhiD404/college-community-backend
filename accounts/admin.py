from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_superuser', 'is_email_verified')
    search_fields = ('email', 'username')
    ordering = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_email_verified', 'department')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('department', 'batch')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'is_email_verified', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active', 'is_email_verified', 'department', 'batch'),
        }),
    )
