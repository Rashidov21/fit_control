"""
URLs for superuser gym management.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .superuser_views import SuperuserGymViewSet
from .public_views import public_register_gym

router = DefaultRouter()
router.register(r'gyms', SuperuserGymViewSet, basename='superuser-gym')

urlpatterns = [
    path('', include(router.urls)),
    path('public/register/', public_register_gym, name='public_register_gym'),
]
