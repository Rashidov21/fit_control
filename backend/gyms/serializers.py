"""
Serializers for gym models.
"""
from rest_framework import serializers
from .models import Gym
from subscriptions.serializers import SubscriptionPlanSerializer


class GymSerializer(serializers.ModelSerializer):
    """Serializer for Gym model."""
    subscription_status = serializers.CharField(read_only=True)
    is_subscription_active = serializers.BooleanField(read_only=True)
    subscription_plan_details = SubscriptionPlanSerializer(source='subscription_plan', read_only=True)
    statistics = serializers.SerializerMethodField()
    
    class Meta:
        model = Gym
        fields = [
            'id', 'name', 'address', 'phone', 'email',
            'created_at', 'updated_at', 'is_active',
            'subscription_plan', 'subscription_plan_details',
            'subscription_start_date', 'subscription_end_date',
            'is_trial', 'trial_start_date', 'trial_end_date',
            'subscription_status', 'is_subscription_active',
            'statistics'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_statistics(self, obj):
        """Get gym statistics."""
        return obj.get_statistics()


class GymCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating gym with trial."""
    class Meta:
        model = Gym
        fields = ['name', 'address', 'phone', 'email']
    
    def create(self, validated_data):
        """Create gym and start trial."""
        gym = Gym.objects.create(**validated_data)
        gym.start_trial()
        return gym


class GymStatisticsSerializer(serializers.Serializer):
    """Serializer for gym statistics."""
    clients_count = serializers.IntegerField()
    total_income = serializers.FloatField()
    total_expenses = serializers.FloatField()
    profit = serializers.FloatField()
