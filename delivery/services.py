from typing import Dict, List
from django.utils import timezone
from alerts.models import Alert, UserAlertPreference
from delivery.models import NotificationDelivery
from delivery.channels.base import NotificationChannel
from delivery.channels.in_app import InAppNotificationChannel
from delivery.channels.email import EmailNotificationChannel
from delivery.channels.sms import SMSNotificationChannel

class NotificationService:
    """Service class to manage different notification channels - Strategy Pattern Context"""
    
    def __init__(self):
        self._channels: Dict[str, NotificationChannel] = {
            NotificationDelivery.Channel.INAPP: InAppNotificationChannel(),
            NotificationDelivery.Channel.EMAIL: EmailNotificationChannel(),
            NotificationDelivery.Channel.SMS: SMSNotificationChannel(),
        }
    
    def add_channel(self, channel: NotificationChannel):
        """Add a new notification channel"""
        self._channels[channel.get_channel_type()] = channel
    
    def send_alert(self, alert: Alert) -> List[NotificationDelivery]:
        """Send alert through appropriate channel"""
        if not alert.is_current:
            return []
        
        target_users = list(alert.get_target_users())
        
        # Map delivery type to channel
        channel_type = alert.delivery_type
        channel = self._channels.get(channel_type)
        
        if not channel:
            raise ValueError(f"Unsupported delivery type: {channel_type}")
        
        return channel.send_notification(alert, target_users)
    
    def send_reminders(self):
        """Send reminders for all active alerts that need them"""
        # Get all preferences that need reminders
        preferences = UserAlertPreference.objects.select_related('alert', 'user').filter(
            alert__is_active=True,
            alert__reminder_enabled=True,
            alert__start_time__lte=timezone.now(),
            alert__expiry_time__gt=timezone.now(),
            is_read=False
        )
        
        reminders_sent = []
        for preference in preferences:
            if preference.should_send_reminder:
                try:
                    deliveries = self.send_alert(preference.alert)
                    reminders_sent.extend(deliveries)
                except Exception as e:
                    # Log error but continue with other reminders
                    print(f"Error sending reminder for alert {preference.alert.id}: {e}")
        
        return reminders_sent
