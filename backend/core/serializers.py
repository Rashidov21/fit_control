"""
Serializers for core models.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, QRCode


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    gym_name = serializers.CharField(source='gym.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'gym', 'gym_name', 'is_gym_admin', 'telegram_id', 'telegram_username']
        read_only_fields = ['id']


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password.')
        
        return attrs


class QRCodeSerializer(serializers.ModelSerializer):
    """Serializer for QRCode model."""
    qr_url = serializers.CharField(read_only=True)
    gym_name = serializers.CharField(source='gym.name', read_only=True)
    
    class Meta:
        model = QRCode
        fields = ['id', 'gym', 'gym_name', 'token', 'qr_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'token', 'created_at', 'updated_at']
