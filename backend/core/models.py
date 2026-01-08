"""
Core models for the Fitness Club Management Platform.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import secrets


class User(AbstractUser):
    """Custom user model with gym association."""
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    is_gym_admin = models.BooleanField(default=False)
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True)
    telegram_username = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username


class QRCode(models.Model):
    """QR code for gym authentication."""
    gym = models.OneToOneField('gyms.Gym', on_delete=models.CASCADE, related_name='qr_code')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'QR Code'
        verbose_name_plural = 'QR Codes'
    
    def __str__(self):
        return f"QR Code for {self.gym.name}"
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)
    
    @property
    def qr_url(self):
        """Generate QR code URL for Telegram deep linking."""
        from django.conf import settings
        bot_username = settings.TELEGRAM_BOT_USERNAME
        return f"https://t.me/{bot_username}?start={self.token}"
