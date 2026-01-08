from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Admin interface for Client model."""
    list_display = ['full_name', 'phone', 'gym', 'registration_date', 'is_active']
    list_filter = ['gym', 'is_active', 'registration_date']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    readonly_fields = ['registration_date']
