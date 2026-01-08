"""
Gym models for multi-tenant system.
"""
from django.db import models
from django.utils import timezone
from django.conf import settings


class Gym(models.Model):
    """Gym model representing a tenant."""
    name = models.CharField(max_length=255, verbose_name='Gym Name')
    address = models.TextField(blank=True, verbose_name='Address')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Phone')
    email = models.EmailField(blank=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    
    # Subscription info
    subscription_plan = models.ForeignKey(
        'subscriptions.SubscriptionPlan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='gyms',
        verbose_name='Subscription Plan'
    )
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    is_trial = models.BooleanField(default=True, verbose_name='Is Trial')
    trial_start_date = models.DateTimeField(null=True, blank=True)
    trial_end_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Gym'
        verbose_name_plural = 'Gyms'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def subscription_status(self):
        """Get current subscription status."""
        now = timezone.now()
        
        # Check if in trial period
        if self.is_trial and self.trial_end_date:
            if now < self.trial_end_date:
                return 'trial'
            elif now >= self.trial_end_date and not self.subscription_plan:
                return 'expired'
        
        # Check subscription
        if self.subscription_plan:
            if self.subscription_end_date and now < self.subscription_end_date:
                return 'active'
            elif self.subscription_end_date and now >= self.subscription_end_date:
                return 'expired'
        
        return 'expired'
    
    @property
    def is_subscription_active(self):
        """Check if subscription is currently active."""
        return self.subscription_status == 'active' or self.subscription_status == 'trial'
    
    def start_trial(self):
        """Start 14-day free trial."""
        from django.conf import settings
        from datetime import timedelta
        
        self.is_trial = True
        self.trial_start_date = timezone.now()
        self.trial_end_date = self.trial_start_date + timedelta(days=settings.TRIAL_PERIOD_DAYS)
        self.save()
    
    def assign_subscription(self, plan, start_date=None):
        """Assign subscription plan to gym."""
        from datetime import timedelta
        
        self.subscription_plan = plan
        self.subscription_start_date = start_date or timezone.now()
        
        if plan.plan_type == 'monthly':
            self.subscription_end_date = self.subscription_start_date + timedelta(days=30)
        elif plan.plan_type == 'yearly':
            self.subscription_end_date = self.subscription_start_date + timedelta(days=365)
        elif plan.plan_type == 'lifetime':
            # Set far future date for lifetime
            self.subscription_end_date = timezone.now() + timedelta(days=36500)  # ~100 years
        
        self.is_trial = False
        self.save()
    
    def get_statistics(self):
        """Get gym statistics."""
        from clients.models import Client
        from payments.models import Payment
        from expenses.models import Expense
        from django.db.models import Sum
        
        clients_count = Client.objects.filter(gym=self).count()
        total_income = Payment.objects.filter(gym=self).aggregate(
            total=Sum('amount')
        )['total'] or 0
        total_expenses = Expense.objects.filter(gym=self).aggregate(
            total=Sum('amount')
        )['total'] or 0
        profit = total_income - total_expenses
        
        return {
            'clients_count': clients_count,
            'total_income': float(total_income),
            'total_expenses': float(total_expenses),
            'profit': float(profit),
        }


class TrialRequest(models.Model):
    """Trial request model for minimal registration."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    name = models.CharField(max_length=255, verbose_name='Name')
    phone = models.CharField(max_length=20, verbose_name='Phone')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    admin_notes = models.TextField(blank=True, verbose_name='Admin Notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # If approved, link to gym
    gym = models.ForeignKey(
        'Gym',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trial_requests',
        verbose_name='Gym'
    )
    
    class Meta:
        verbose_name = 'Trial Request'
        verbose_name_plural = 'Trial Requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.phone} ({self.status})"