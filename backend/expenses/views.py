"""
API views for expense management.
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet for expense management."""
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gym', 'category', 'expense_date']
    search_fields = ['category', 'description']
    ordering_fields = ['expense_date', 'amount', 'created_at']
    ordering = ['-expense_date', '-created_at']
    
    def get_queryset(self):
        """Get expenses for current user's gym."""
        if self.request.user.is_superuser:
            return Expense.objects.all()
        elif self.request.user.is_gym_admin and self.request.user.gym:
            return Expense.objects.filter(gym=self.request.user.gym)
        return Expense.objects.none()
    
    def perform_create(self, serializer):
        """Set gym when creating expense."""
        if not self.request.user.is_superuser:
            serializer.save(gym=self.request.user.gym)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get expense statistics."""
        queryset = self.get_queryset()
        
        total_expenses = queryset.aggregate(total=Sum('amount'))['total'] or 0
        
        # Monthly statistics
        from django.utils import timezone
        from datetime import timedelta
        
        current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_expenses = queryset.filter(
            expense_date__gte=current_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Category breakdown
        category_breakdown = queryset.values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        return Response({
            'total_expenses': float(total_expenses),
            'monthly_expenses': float(monthly_expenses),
            'total_expense_records': queryset.count(),
            'category_breakdown': list(category_breakdown),
        })
