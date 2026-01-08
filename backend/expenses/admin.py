from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Admin interface for Expense model."""
    list_display = ['category', 'amount', 'expense_date', 'gym', 'created_at']
    list_filter = ['gym', 'category', 'expense_date', 'created_at']
    search_fields = ['category', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'expense_date'
