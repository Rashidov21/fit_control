"""
URLs for core authentication.
"""
from django.urls import path
from .views import login_view, logout_view, current_user, QRCodeDetailView, verify_qr_token

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('me/', current_user, name='current_user'),
    path('qr-code/', QRCodeDetailView.as_view(), name='qr_code'),
    path('verify-qr/<str:token>/', verify_qr_token, name='verify_qr'),
]
