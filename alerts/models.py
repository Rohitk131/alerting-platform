from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid

class Alert(models.Model):
    """Main Alert model following OOP principles"""
    
    class Severity(models.TextChoices):
        INFO = 'Info', 'Info'
        WARNING = 'Warning', 'Warning'
        CRITICAL = 'Critical', 'Critical'
    
    class DeliveryType(models.TextChoices):
        INAPP = 'InApp', 'In-App'
        EMAIL = 'Email', 'Email'
        SMS = 'SMS', 'SMS'
    
    class VisibilityType(models.TextChoices):
        ORGANIZATION = 'Organization', 'Organization'
        TEAM = 'Team', 'Team'
        USER = 'User', 'User'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=Severity.choices, default=Severity.INFO)
    delivery_type = models.CharField(max_length=10, choices=DeliveryType.choices, default=DeliveryType.INAPP)
    visibility_type = models.CharField(max_length=15, choices=VisibilityType.choices)
    
    # Visibility targeting
    visible_to_teams = models.ManyToManyField('users.Team', blank=True, related_name='alerts')
    visible_to_users = models.ManyToManyField('users.User', blank=True, related_name='targeted_alerts')
    
    # Timing
    start_time = models.DateTimeField(default=timezone.now)
    expiry_time = models.DateTimeField()
    reminder_frequency = models.PositiveIntegerField(default=120)  # minutes
    reminder_enabled = models.BooleanField(default=True)
    
    # Management
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.severity})"
    
    @property
    def is_expired(self):
        return timezone.now() > self.expiry_time
    
    @property
    def is_current(self):
        now = timezone.now()
        return self.start_time <= now <= self.expiry_time and self.is_active
    
    def get_target_users(self):
        """Get all users who should receive this alert based on visibility settings"""
        from users.models import User
        
        if self.visibility_type == self.VisibilityType.ORGANIZATION:
            return User.objects.all()
        elif self.visibility_type == self.VisibilityType.TEAM:
            return User.objects.filter(team__in=self.visible_to_teams.all())
        elif self.visibility_type == self.VisibilityType.USER:
            return self.visible_to_users.all()
        return User.objects.none()
    
    class Meta:
        db_table = 'alerts'
        ordering = ['-created_at']

class UserAlertPreference(models.Model):
    """User preferences for each alert - State Pattern for read/snooze logic"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='alert_preferences')
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='user_preferences')
    is_read = models.BooleanField(default=False)
    snoozed_until = models.DateField(null=True, blank=True)
    last_reminder_sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.alert.title} ({'Read' if self.is_read else 'Unread'})"
    
    def snooze_for_day(self):
        """Snooze alert until end of current day"""
        tomorrow = timezone.now().date() + timedelta(days=1)
        self.snoozed_until = tomorrow
        self.save()
    
    def unsnooze(self):
        """Remove snooze status"""
        self.snoozed_until = None
        self.save()
    
    @property
    def is_snoozed(self):
        """Check if currently snoozed"""
        if not self.snoozed_until:
            return False
        return timezone.now().date() < self.snoozed_until
    
    @property
    def should_send_reminder(self):
        """Check if reminder should be sent based on snooze and timing"""
        if self.is_snoozed:
            return False
        
        if not self.last_reminder_sent_at:
            return True
        
        time_since_last_reminder = timezone.now() - self.last_reminder_sent_at
        reminder_interval = timedelta(minutes=self.alert.reminder_frequency)
        return time_since_last_reminder >= reminder_interval
    
    def mark_read(self):
        """Mark alert as read"""
        self.is_read = True
        self.save()
    
    def mark_unread(self):
        """Mark alert as unread"""
        self.is_read = False
        self.save()
    
    class Meta:
        db_table = 'user_alert_preferences'
        unique_together = ['user', 'alert']