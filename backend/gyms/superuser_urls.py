"""
URLs for superuser gym management.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .superuser_views import SuperuserGymViewSet, TrialRequestViewSet
from .public_views import public_register_gym, public_register_trial_request

router = DefaultRouter()
router.register(r'gyms', SuperuserGymViewSet, basename='superuser-gym')
router.register(r'trial-requests', TrialRequestViewSet, basename='trial-request')

urlpatterns = [
    path('', include(router.urls)),
    path('public/register/', public_register_gym, name='public_register_gym'),
    path('public/trial-request/', public_register_trial_request, name='public_register_trial_request'),
]
