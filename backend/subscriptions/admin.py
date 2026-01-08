from django.contrib import admin
from .models import SubscriptionPlan


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """Admin interface for SubscriptionPlan model."""
    list_display = ['name', 'plan_type', 'price', 'is_active', 'created_at']
    list_filter = ['plan_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
