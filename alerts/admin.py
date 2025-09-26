from django.contrib import admin
from alerts.models import Alert, UserAlertPreference

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'severity', 'visibility_type', 'is_active', 'is_current', 'created_at']
    list_filter = ['severity', 'visibility_type', 'is_active', 'delivery_type']
    search_fields = ['title', 'message']
    readonly_fields = ['created_at', 'updated_at', 'is_expired', 'is_current']
    filter_horizontal = ['visible_to_teams', 'visible_to_users']

@admin.register(UserAlertPreference)
class UserAlertPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'alert', 'is_read', 'is_snoozed', 'last_reminder_sent_at']
    list_filter = ['is_read', 'alert__severity']
    search_fields = ['user__username', 'alert__title']
