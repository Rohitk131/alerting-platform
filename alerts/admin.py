from django.contrib import admin
from .models import Alert, UserAlertPreference

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    pass

@admin.register(UserAlertPreference)
class UserAlertPreferenceAdmin(admin.ModelAdmin):
    pass