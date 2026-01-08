"""
API views for superuser gym management.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import User
from django.utils import timezone
from .models import Gym, TrialRequest
from .serializers import GymSerializer, GymCreateSerializer, GymStatisticsSerializer, TrialRequestSerializer
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
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            gym = serializer.save()
            
            # Start trial if not already started
            if gym.is_trial and not gym.trial_start_date:
                gym.start_trial()
            
            # Create QR code for gym
            QRCode.objects.get_or_create(gym=gym)
            
            return Response(
                GymSerializer(gym).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': f'Error creating gym: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def assign_subscription(self, request, pk=None):
        """Assign subscription plan to gym."""
        try:
            gym = self.get_object()
            plan_id = request.data.get('subscription_plan_id')
            
            if not plan_id:
                return Response(
                    {'error': 'subscription_plan_id is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                plan = SubscriptionPlan.objects.get(id=plan_id, is_active=True)
            except SubscriptionPlan.DoesNotExist:
                return Response(
                    {'error': 'Subscription plan not found or inactive.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Validate gym status
            if not gym.is_active:
                return Response(
                    {'error': 'Cannot assign subscription to inactive gym.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            gym.assign_subscription(plan)
            serializer = self.get_serializer(gym)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error assigning subscription: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def create_admin(self, request, pk=None):
        """Create admin user for gym."""
        try:
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
        except Exception as e:
            return Response(
                {'error': f'Error creating admin user: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get gym statistics."""
        try:
            gym = self.get_object()
            stats = gym.get_statistics()
            serializer = GymStatisticsSerializer(stats)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error retrieving statistics: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Get all expired gyms."""
        try:
            expired_gyms = []
            for gym in Gym.objects.all():
                if gym.subscription_status == 'expired':
                    expired_gyms.append(gym)
            
            serializer = self.get_serializer(expired_gyms, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error retrieving expired gyms: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def block_expired(self, request):
        """Block all expired gyms."""
        try:
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
        except Exception as e:
            return Response(
                {'error': f'Error blocking expired gyms: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TrialRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for trial request management (superuser only)."""
    permission_classes = [IsSuperuser]
    serializer_class = TrialRequestSerializer
    
    def get_queryset(self):
        """Get all trial requests (superuser only)."""
        if not self.request.user.is_superuser:
            return TrialRequest.objects.none()
        return TrialRequest.objects.all().order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve trial request and create gym with admin user."""
        try:
            trial_request = self.get_object()
            
            if trial_request.status != 'pending':
                return Response(
                    {'error': 'Only pending requests can be approved.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get admin user data from request
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email', '')
            
            if not username or not password:
                return Response(
                    {'error': 'username and password are required for admin user.'},
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
                name=trial_request.name,
                phone=trial_request.phone,
                email=email
            )
            
            # Start trial
            gym.start_trial()
            
            # Create QR code
            QRCode.objects.get_or_create(gym=gym)
            
            # Create admin user
            admin_user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                gym=gym,
                is_gym_admin=True
            )
            
            # Update trial request
            trial_request.status = 'approved'
            trial_request.gym = gym
            trial_request.save()
            
            return Response({
                'message': 'Trial request approved. Gym and admin user created successfully.',
                'trial_request': TrialRequestSerializer(trial_request).data,
                'gym': GymSerializer(gym).data,
                'admin_username': username
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error approving trial request: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject trial request."""
        try:
            trial_request = self.get_object()
            
            if trial_request.status != 'pending':
                return Response(
                    {'error': 'Only pending requests can be rejected.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            admin_notes = request.data.get('admin_notes', '')
            trial_request.status = 'rejected'
            if admin_notes:
                trial_request.admin_notes = admin_notes
            trial_request.save()
            
            return Response({
                'message': 'Trial request rejected.',
                'trial_request': TrialRequestSerializer(trial_request).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error rejecting trial request: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
