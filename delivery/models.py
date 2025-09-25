import uuid
from django.db import models
from users.models import User
from alerts.models import Alert


class NotificationDelivery(models.Model):
    class Channel(models.TextChoices):
        IN_APP = "IN_APP", "In-App"
        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "SMS"

    class Status(models.TextChoices):
        DELIVERED = "DELIVERED", "Delivered"
        FAILED = "FAILED", "Failed"
        PENDING = "PENDING", "Pending"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=20, choices=Channel.choices, default=Channel.IN_APP)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    sent_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.alert.title} -> {self.user.username} [{self.channel}]"
