"""
API views for subscription management.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from .models import SubscriptionPlan
from .serializers import SubscriptionPlanSerializer


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    """ViewSet for subscription plan management."""
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'list':
            # Allow public access to list plans
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Get subscription plans."""
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return SubscriptionPlan.objects.all()
        return SubscriptionPlan.objects.filter(is_active=True)
