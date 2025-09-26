from django.core.management.base import BaseCommand
from delivery.services import NotificationService

class Command(BaseCommand):
    help = 'Send reminder notifications for active alerts'
    
    def handle(self, *args, **options):
        notification_service = NotificationService()
        deliveries = notification_service.send_reminders()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {len(deliveries)} reminder notifications')
        )
