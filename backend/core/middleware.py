"""
Middleware for multi-tenant gym isolation.
"""
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


class GymMiddleware(MiddlewareMixin):
    """
    Middleware to set current gym context for multi-tenant isolation.
    """
    def process_request(self, request):
        """Set gym context based on user's gym association."""
        if request.user.is_authenticated and request.user.gym:
            request.gym = request.user.gym
        elif request.user.is_authenticated and request.user.is_superuser:
            # Superuser can access all gyms
            request.gym = None
        else:
            request.gym = None
