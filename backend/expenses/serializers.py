"""
Serializers for expense models.
"""
from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense model."""
    gym_name = serializers.CharField(source='gym.name', read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            'id', 'gym', 'gym_name', 'category', 'amount',
            'description', 'expense_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
