from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for Payment model."""
    list_display = ['client', 'amount', 'payment_date', 'gym', 'created_at']
    list_filter = ['gym', 'payment_date', 'created_at']
    search_fields = ['client__first_name', 'client__last_name', 'client__phone']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'payment_date'
