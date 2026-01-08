"""
Subscription models.
"""
from django.db import models


class SubscriptionPlan(models.Model):
    """Subscription plan model."""
    PLAN_TYPES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('lifetime', 'Lifetime'),
    ]
    
    name = models.CharField(max_length=255, verbose_name='Plan Name')
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, verbose_name='Plan Type')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    description = models.TextField(blank=True, verbose_name='Description')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} ({self.plan_type})"
