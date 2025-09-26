from typing import List
from django.utils import timezone
from delivery.models import NotificationDelivery
from alerts.models import Alert, UserAlertPreference
from delivery.channels.base import NotificationChannel

class InAppNotificationChannel(NotificationChannel):
    """In-app notification channel implementation"""
    
    def send_notification(self, alert: Alert, users: List) -> List[NotificationDelivery]:
        """Send in-app notifications to users"""
        deliveries = []
        
        for user in users:
            # Create or get user preference
            preference, created = UserAlertPreference.objects.get_or_create(
                user=user,
                alert=alert,
                defaults={'is_read': False}
            )
            
            # Create delivery record
            delivery = NotificationDelivery.objects.create(
                alert=alert,
                user=user,
                channel=NotificationDelivery.Channel.INAPP,
                status=NotificationDelivery.Status.DELIVERED
            )
            
            # Update last reminded time
            preference.last_reminder_sent_at = timezone.now()
            
            # Reset snooze if it's a new day
            if preference.is_snoozed and preference.snoozed_until and timezone.now().date() >= preference.snoozed_until:
                preference.unsnooze()
            
            preference.save()
            deliveries.append(delivery)
        
        return deliveries
    
    def get_channel_type(self) -> str:
        return NotificationDelivery.Channel.INAPP