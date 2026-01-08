from django.contrib import admin
from .models import Gym, TrialRequest


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    """Admin interface for Gym model."""
    list_display = ['name', 'phone', 'email', 'subscription_status', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_trial', 'subscription_plan', 'created_at']
    search_fields = ['name', 'phone', 'email', 'address']
    readonly_fields = ['created_at', 'updated_at', 'subscription_status', 'is_subscription_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'phone', 'email', 'is_active')
        }),
        ('Subscription', {
            'fields': (
                'subscription_plan',
                'subscription_start_date',
                'subscription_end_date',
                'is_trial',
                'trial_start_date',
                'trial_end_date',
                'subscription_status',
                'is_subscription_active'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(TrialRequest)
class TrialRequestAdmin(admin.ModelAdmin):
    """Admin interface for TrialRequest model."""
    list_display = ['name', 'phone', 'status', 'gym', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('name', 'phone', 'status')
        }),
        ('Admin', {
            'fields': ('gym', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
