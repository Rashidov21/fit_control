"""
Management command to check and block expired subscriptions.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from gyms.models import Gym


class Command(BaseCommand):
    help = 'Check and block gyms with expired subscriptions'
    
    def handle(self, *args, **options):
        """Check all gyms and block expired ones."""
        blocked_count = 0
        checked_count = 0
        
        for gym in Gym.objects.all():
            checked_count += 1
            status = gym.subscription_status
            
            if status == 'expired' and gym.is_active:
                gym.is_active = False
                gym.save()
                blocked_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Blocked gym: {gym.name} (ID: {gym.id})')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Checked {checked_count} gyms. Blocked {blocked_count} expired gyms.'
            )
        )
