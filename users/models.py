from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Team(models.Model):
    """Team model for organizing users"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'teams'

class User(AbstractUser):
    """Custom User model extending AbstractUser"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.username} ({self.team.name if self.team else 'No Team'})"
    
    class Meta:
        db_table = 'users'