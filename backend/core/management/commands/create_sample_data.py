"""
Management command to create sample data for testing.
"""
from django.core.management.base import BaseCommand
from core.models import User
from gyms.models import Gym
from subscriptions.models import SubscriptionPlan
from core.models import QRCode


class Command(BaseCommand):
    help = 'Create sample data for testing'
    
    def handle(self, *args, **options):
        """Create sample subscription plans and gym."""
        
        # Create subscription plans
        monthly_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Oylik',
            defaults={
                'plan_type': 'monthly',
                'price': 500000.00,
                'description': 'Oylik obuna rejasi',
                'is_active': True
            }
        )
        
        yearly_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Yillik',
            defaults={
                'plan_type': 'yearly',
                'price': 5000000.00,
                'description': 'Yillik obuna rejasi',
                'is_active': True
            }
        )
        
        lifetime_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Umrbod',
            defaults={
                'plan_type': 'lifetime',
                'price': 50000000.00,
                'description': 'Umrbod obuna rejasi',
                'is_active': True
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS('Sample subscription plans created/updated.')
        )
        
        # Create sample gym if it doesn't exist
        if not Gym.objects.filter(name='Sample Gym').exists():
            gym = Gym.objects.create(
                name='Sample Gym',
                address='Toshkent shahri',
                phone='+998901234567',
                email='sample@gym.uz'
            )
            gym.start_trial()
            
            # Create QR code
            QRCode.objects.get_or_create(gym=gym)
            
            # Create admin user
            if not User.objects.filter(username='admin').exists():
                admin_user = User.objects.create_user(
                    username='admin',
                    password='admin123',
                    email='admin@gym.uz',
                    gym=gym,
                    is_gym_admin=True
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Sample gym created with admin user: admin/admin123'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS('Sample data creation completed!')
        )
