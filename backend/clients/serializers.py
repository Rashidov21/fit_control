"""
Serializers for client models.
"""
from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model."""
    full_name = serializers.CharField(read_only=True)
    gym_name = serializers.CharField(source='gym.name', read_only=True)
    
    class Meta:
        model = Client
        fields = [
            'id', 'gym', 'gym_name', 'first_name', 'last_name', 'full_name',
            'phone', 'email', 'telegram_id', 'telegram_username',
            'registration_date', 'is_active', 'notes'
        ]
        read_only_fields = ['id', 'registration_date']
