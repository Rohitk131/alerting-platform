import uuid
from django.db import models
from users.models import User, Team


class Alert(models.Model):
    class Severity(models.TextChoices):
        INFO = "INFO", "Info"
        WARNING = "WARNING", "Warning"
        CRITICAL = "CRITICAL", "Critical"

    class DeliveryType(models.TextChoices):
        IN_APP = "IN_APP", "In-App"
        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "SMS"

    class VisibilityType(models.TextChoices):
        ORG = "ORG", "Organization"
        TEAM = "TEAM", "Team"
        USER = "USER", "User"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=Severity.choices)
    delivery_type = models.CharField(max_length=20, choices=DeliveryType.choices, default=DeliveryType.IN_APP)
    visibility_type = models.CharField(max_length=20, choices=VisibilityType.choices)

    visible_to_teams = models.ManyToManyField(Team, blank=True, related_name="alerts")
    visible_to_users = models.ManyToManyField(User, blank=True, related_name="alerts")

    start_time = models.DateTimeField()
    expiry_time = models.DateTimeField()

    reminder_frequency = models.PositiveIntegerField(default=120, help_text="Frequency in minutes")
    reminder_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.severity})"


class UserAlertPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    snoozed_until = models.DateField(null=True, blank=True)
    last_reminder_sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "alert")

    def __str__(self):
        return f"{self.user.username} - {self.alert.title}"
