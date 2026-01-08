"""
Serializers for subscription models.
"""
from rest_framework import serializers
from .models import SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Serializer for SubscriptionPlan model."""
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'plan_type', 'price', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
