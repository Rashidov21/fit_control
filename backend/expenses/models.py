"""
Expense models.
"""
from django.db import models
from django.utils import timezone


class Expense(models.Model):
    """Expense model for tracking gym expenses."""
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=255, verbose_name='Category')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    description = models.TextField(blank=True, verbose_name='Description')
    expense_date = models.DateField(default=timezone.now, verbose_name='Expense Date')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['-expense_date', '-created_at']
    
    def __str__(self):
        return f"{self.category} - {self.amount} ({self.expense_date})"
