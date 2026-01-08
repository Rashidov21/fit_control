"""
Custom permission classes.
"""
from rest_framework import permissions


class IsSuperuser(permissions.BasePermission):
    """Permission class to check if user is superuser."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser


class IsGymAdmin(permissions.BasePermission):
    """Permission class to check if user is gym admin."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_gym_admin
