"""
Payment models.
"""
from django.db import models
from django.utils import timezone


class Payment(models.Model):
    """Payment model for tracking client payments."""
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='payments')
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    payment_date = models.DateField(default=timezone.now, verbose_name='Payment Date')
    notes = models.TextField(blank=True, verbose_name='Notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date', '-created_at']
    
    def __str__(self):
        return f"{self.client.full_name} - {self.amount} ({self.payment_date})"
