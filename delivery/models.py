from django.db import models
import uuid

class NotificationDelivery(models.Model):
    """Log of each alert sent to a user - Strategy Pattern for delivery channels"""
    
    class Channel(models.TextChoices):
        INAPP = 'InApp', 'In-App'
        EMAIL = 'Email', 'Email'
        SMS = 'SMS', 'SMS'
    
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        DELIVERED = 'Delivered', 'Delivered'
        FAILED = 'Failed', 'Failed'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alert = models.ForeignKey('alerts.Alert', on_delete=models.CASCADE, related_name='deliveries')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='alert_deliveries')
    channel = models.CharField(max_length=10, choices=Channel.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    sent_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.alert.title} -> {self.user.username} ({self.status})"
    
    class Meta:
        db_table = 'notification_deliveries'