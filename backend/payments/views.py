"""
API views for payment management.
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for payment management."""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gym', 'client', 'payment_date']
    search_fields = ['client__first_name', 'client__last_name', 'client__phone']
    ordering_fields = ['payment_date', 'amount', 'created_at']
    ordering = ['-payment_date', '-created_at']
    
    def get_queryset(self):
        """Get payments for current user's gym."""
        if self.request.user.is_superuser:
            return Payment.objects.all()
        elif self.request.user.is_gym_admin and self.request.user.gym:
            return Payment.objects.filter(gym=self.request.user.gym)
        return Payment.objects.none()
    
    def perform_create(self, serializer):
        """Set gym when creating payment."""
        if not self.request.user.is_superuser:
            serializer.save(gym=self.request.user.gym)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get payment statistics."""
        queryset = self.get_queryset()
        
        total_income = queryset.aggregate(total=Sum('amount'))['total'] or 0
        
        # Monthly statistics
        from django.utils import timezone
        from django.db.models import Sum
        from datetime import timedelta
        
        current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_income = queryset.filter(
            payment_date__gte=current_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'total_income': float(total_income),
            'monthly_income': float(monthly_income),
            'total_payments': queryset.count(),
        })
