"""
API views for client management.
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet for client management."""
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'gym']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    ordering_fields = ['registration_date', 'first_name', 'last_name']
    ordering = ['-registration_date']
    
    def get_queryset(self):
        """Get clients for current user's gym."""
        if self.request.user.is_superuser:
            return Client.objects.all()
        elif self.request.user.is_gym_admin and self.request.user.gym:
            return Client.objects.filter(gym=self.request.user.gym)
        return Client.objects.none()
    
    def perform_create(self, serializer):
        """Set gym when creating client."""
        if not self.request.user.is_superuser:
            serializer.save(gym=self.request.user.gym)
        else:
            serializer.save()
