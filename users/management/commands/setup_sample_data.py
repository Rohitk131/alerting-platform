from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import User, Team
from alerts.models import Alert

class Command(BaseCommand):
    help = 'Setup sample data for testing'
    
    def handle(self, *args, **options):
        # Create teams
        engineering_team, _ = Team.objects.get_or_create(
            name='Engineering'
        )
        
        marketing_team, _ = Team.objects.get_or_create(
            name='Marketing'
        )
        
        operations_team, _ = Team.objects.get_or_create(
            name='Operations'
        )
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            email='admin@company.com',
            defaults={
                'first_name': 'System',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
                'is_admin': True,
                'team': engineering_team
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        
        # Create regular users
        users_data = [
            ('john_doe', 'john@company.com', 'John', 'Doe', engineering_team),
            ('jane_smith', 'jane@company.com', 'Jane', 'Smith', engineering_team),
            ('mike_wilson', 'mike@company.com', 'Mike', 'Wilson', marketing_team),
            ('sarah_johnson', 'sarah@company.com', 'Sarah', 'Johnson', marketing_team),
            ('tom_brown', 'tom@company.com', 'Tom', 'Brown', operations_team),
        ]
        
        for username, email, first_name, last_name, team in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'team': team
                }
            )
            if created:
                user.set_password('password123')
                user.save()
        
        # Create sample alerts
        now = timezone.now()
        
        # Organization-wide critical alert
        alert1, _ = Alert.objects.get_or_create(
            title='System Maintenance Scheduled',
            defaults={
                'message': 'Our systems will undergo scheduled maintenance this weekend. Please save your work and log out by Friday 6 PM.',
                'severity': Alert.Severity.CRITICAL,
                'visibility_type': Alert.VisibilityType.ORGANIZATION,
                'start_time': now,
                'expiry_time': now + timedelta(days=7)
            }
        )
        
        # Team-specific warning
        alert2, created = Alert.objects.get_or_create(
            title='Code Review Deadline Approaching',
            defaults={
                'message': 'Please complete all pending code reviews by end of this week.',
                'severity': Alert.Severity.WARNING,
                'visibility_type': Alert.VisibilityType.TEAM,
                'start_time': now,
                'expiry_time': now + timedelta(days=3)
            }
        )
        if created:
            alert2.visible_to_teams.add(engineering_team)
        
        # User-specific info alert
        john_user = User.objects.get(username='john_doe')
        alert3, created = Alert.objects.get_or_create(
            title='Welcome to the Platform',
            defaults={
                'message': 'Welcome! Please complete your profile setup.',
                'severity': Alert.Severity.INFO,
                'visibility_type': Alert.VisibilityType.USER,
                'start_time': now,
                'expiry_time': now + timedelta(days=30)
            }
        )
        if created:
            alert3.visible_to_users.add(john_user)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
