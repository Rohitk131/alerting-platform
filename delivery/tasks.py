from celery import shared_task
from django.utils import timezone
from delivery.services import NotificationService

@shared_task
def send_reminder_notifications():
    """Celery task to send reminder notifications every 2 hours"""
    notification_service = NotificationService()
    deliveries = notification_service.send_reminders()
    return f"Sent {len(deliveries)} reminder notifications"

@shared_task  
def cleanup_expired_alerts():
    """Celery task to cleanup expired alerts"""
    from alerts.models import Alert
    
    expired_count = Alert.objects.filter(
        expiry_time__lt=timezone.now(),
        is_active=True
    ).update(is_active=False)
    
    return f"Deactivated {expired_count} expired alerts"