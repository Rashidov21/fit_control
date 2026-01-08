from django.contrib import admin
from .models import Gym


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
