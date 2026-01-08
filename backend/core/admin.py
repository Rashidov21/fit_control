from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, QRCode


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    list_display = ['username', 'email', 'gym', 'is_gym_admin', 'is_superuser', 'is_active']
    list_filter = ['is_gym_admin', 'is_superuser', 'is_active', 'gym']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Gym Information', {'fields': ('gym', 'is_gym_admin', 'telegram_id', 'telegram_username')}),
    )


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    """Admin interface for QRCode model."""
    list_display = ['gym', 'token', 'created_at']
    readonly_fields = ['token', 'created_at', 'updated_at']
