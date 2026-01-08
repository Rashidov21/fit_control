"""
API views for superuser gym management.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Gym
from .serializers import GymSerializer, GymCreateSerializer, GymStatisticsSerializer
from subscriptions.models import SubscriptionPlan
from core.models import QRCode
from core.permissions import IsSuperuser


class SuperuserGymViewSet(viewsets.ModelViewSet):
    """ViewSet for superuser gym management."""
    permission_classes = [IsSuperuser]
    
    def get_queryset(self):
        """Get all gyms (superuser only)."""
        if not self.request.user.is_superuser:
            return Gym.objects.none()
        return Gym.objects.all()
    
    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action == 'create':
            return GymCreateSerializer
        return GymSerializer
    
    def create(self, request, *args, **kwargs):
        """Create gym with trial."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gym = serializer.save()
        
        # Create QR code for gym
        QRCode.objects.get_or_create(gym=gym)
        
        return Response(
            GymSerializer(gym).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def assign_subscription(self, request, pk=None):
        """Assign subscription plan to gym."""
        gym = self.get_object()
        plan_id = request.data.get('subscription_plan_id')
        
        if not plan_id:
            return Response(
                {'error': 'subscription_plan_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response(
                {'error': 'Subscription plan not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        gym.assign_subscription(plan)
        serializer = self.get_serializer(gym)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def create_admin(self, request, pk=None):
        """Create admin user for gym."""
        gym = self.get_object()
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        
        if not username or not password:
            return Response(
                {'error': 'username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            gym=gym,
            is_gym_admin=True
        )
        
        from core.serializers import UserSerializer
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get gym statistics."""
        gym = self.get_object()
        stats = gym.get_statistics()
        serializer = GymStatisticsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Get all expired gyms."""
        expired_gyms = []
        for gym in Gym.objects.all():
            if gym.subscription_status == 'expired':
                expired_gyms.append(gym)
        
        serializer = self.get_serializer(expired_gyms, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def block_expired(self, request):
        """Block all expired gyms."""
        blocked_count = 0
        for gym in Gym.objects.all():
            if gym.subscription_status == 'expired':
                gym.is_active = False
                gym.save()
                blocked_count += 1
        
        return Response({
            'message': f'Blocked {blocked_count} expired gyms.',
            'blocked_count': blocked_count
        })
