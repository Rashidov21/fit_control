"""
Public views for landing page registration.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Gym
from .serializers import GymSerializer
from core.models import QRCode


@api_view(['POST'])
@permission_classes([AllowAny])
def public_register_gym(request):
    """Public endpoint for gym registration from landing page."""
    name = request.data.get('name')
    address = request.data.get('address', '')
    phone = request.data.get('phone', '')
    email = request.data.get('email', '')
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not name or not username or not password:
        return Response(
            {'error': 'name, username, and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create gym
    gym = Gym.objects.create(
        name=name,
        address=address,
        phone=phone,
        email=email
    )
    
    # Start trial
    gym.start_trial()
    
    # Create QR code
    QRCode.objects.get_or_create(gym=gym)
    
    # Create admin user
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        gym=gym,
        is_gym_admin=True
    )
    
    serializer = GymSerializer(gym)
    return Response({
        'gym': serializer.data,
        'message': 'Gym and admin user created successfully. 14-day trial started.',
    }, status=status.HTTP_201_CREATED)
