"""
API views for gym management.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import User
from .models import Gym
from .serializers import GymSerializer, GymStatisticsSerializer
from subscriptions.models import SubscriptionPlan


class GymViewSet(viewsets.ModelViewSet):
    """ViewSet for gym management (gym admin)."""
    serializer_class = GymSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get gyms accessible to current user."""
        if self.request.user.is_superuser:
            return Gym.objects.all()
        elif self.request.user.is_gym_admin and self.request.user.gym:
            return Gym.objects.filter(id=self.request.user.gym.id)
        return Gym.objects.none()
    
    def get_object(self):
        """Get gym object."""
        if self.request.user.is_superuser:
            return super().get_object()
        return self.request.user.gym
    
    @action(detail=False, methods=['get'])
    def my_gym(self, request):
        """Get current user's gym."""
        try:
            if not request.user.gym:
                return Response(
                    {'error': 'No gym associated with this user.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.get_serializer(request.user.gym)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error retrieving gym: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get gym statistics."""
        try:
            gym = request.user.gym
            if not gym:
                return Response(
                    {'error': 'No gym associated with this user.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            stats = gym.get_statistics()
            serializer = GymStatisticsSerializer(stats)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error retrieving statistics: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def subscription_status(self, request):
        """Get subscription status."""
        try:
            gym = request.user.gym
            if not gym:
                return Response(
                    {'error': 'No gym associated with this user.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response({
                'status': gym.subscription_status,
                'is_active': gym.is_subscription_active,
                'subscription_plan': gym.subscription_plan.name if gym.subscription_plan else None,
                'subscription_end_date': gym.subscription_end_date,
                'trial_end_date': gym.trial_end_date,
            })
        except Exception as e:
            return Response(
                {'error': f'Error retrieving subscription status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
