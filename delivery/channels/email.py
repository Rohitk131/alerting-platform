from typing import List
from delivery.models import NotificationDelivery
from alerts.models import Alert
from delivery.channels.base import NotificationChannel

class EmailNotificationChannel(NotificationChannel):
    """Email notification channel - Future implementation"""
    
    def send_notification(self, alert: Alert, users: List) -> List[NotificationDelivery]:
        """Send email notifications to users"""
        deliveries = []
        
        for user in users:
            try:
                # Future implementation for email sending
                # send_mail(subject=alert.title, message=alert.message, recipient_list=[user.email])
                
                delivery = NotificationDelivery.objects.create(
                    alert=alert,
                    user=user,
                    channel=NotificationDelivery.Channel.EMAIL,
                    status=NotificationDelivery.Status.DELIVERED
                )
                deliveries.append(delivery)
                
            except Exception as e:
                delivery = NotificationDelivery.objects.create(
                    alert=alert,
                    user=user,
                    channel=NotificationDelivery.Channel.EMAIL,
                    status=NotificationDelivery.Status.FAILED,
                    error_message=str(e)
                )
                deliveries.append(delivery)
        
        return deliveries
    
    def get_channel_type(self) -> str:
        return NotificationDelivery.Channel.EMAIL