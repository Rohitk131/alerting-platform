from django.contrib import admin
from delivery.models import NotificationDelivery

@admin.register(NotificationDelivery)
class NotificationDeliveryAdmin(admin.ModelAdmin):
    list_display = ['alert', 'user', 'channel', 'status', 'sent_at']
    list_filter = ['channel', 'status']
    search_fields = ['alert__title', 'user__username']
    readonly_fields = ['sent_at']
