from typing import List
from delivery.models import NotificationDelivery
from alerts.models import Alert
from delivery.channels.base import NotificationChannel


class SMSNotificationChannel(NotificationChannel):
    """SMS notification channel - Future implementation"""
    
    def send_notification(self, alert: Alert, users: List) -> List[NotificationDelivery]:
        """Send SMS notifications to users"""
        deliveries = []
        
        for user in users:
            try:
                # Future implementation for SMS sending
                # send_sms(message=alert.message, phone_number=user.phone_number)
                
                delivery = NotificationDelivery.objects.create(
                    alert=alert,
                    user=user,
                    channel=NotificationDelivery.Channel.SMS,
                    status=NotificationDelivery.Status.DELIVERED
                )
                deliveries.append(delivery)
                
            except Exception as e:
                delivery = NotificationDelivery.objects.create(
                    alert=alert,
                    user=user,
                    channel=NotificationDelivery.Channel.SMS,
                    status=NotificationDelivery.Status.FAILED,
                    error_message=str(e)
                )
                deliveries.append(delivery)
        
        return deliveries
    
    def get_channel_type(self) -> str:
        return NotificationDelivery.Channel.SMS
