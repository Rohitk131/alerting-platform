from django.contrib import admin
from .models import NotificationDelivery

@admin.register(NotificationDelivery)
class NotificationDeliveryAdmin(admin.ModelAdmin):
    pass

