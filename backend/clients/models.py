"""
Client models.
"""
from django.db import models
from django.utils import timezone


class Client(models.Model):
    """Client model."""
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='clients')
    first_name = models.CharField(max_length=255, verbose_name='First Name')
    last_name = models.CharField(max_length=255, verbose_name='Last Name')
    phone = models.CharField(max_length=20, verbose_name='Phone')
    email = models.EmailField(blank=True, verbose_name='Email')
    telegram_id = models.BigIntegerField(null=True, blank=True, verbose_name='Telegram ID')
    telegram_username = models.CharField(max_length=255, null=True, blank=True, verbose_name='Telegram Username')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Registration Date')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    notes = models.TextField(blank=True, verbose_name='Notes')
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['-registration_date']
        unique_together = ['gym', 'phone']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"
    
    @property
    def full_name(self):
        """Get full name."""
        return f"{self.first_name} {self.last_name}"
