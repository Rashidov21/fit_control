"""
Serializers for payment models.
"""
from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model."""
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    client_phone = serializers.CharField(source='client.phone', read_only=True)
    gym_name = serializers.CharField(source='gym.name', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'gym', 'gym_name', 'client', 'client_name', 'client_phone',
            'amount', 'payment_date', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
