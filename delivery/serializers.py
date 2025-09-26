from rest_framework import serializers
from delivery.models import NotificationDelivery
from alerts.serializers import AlertSerializer
from users.serializers import UserSerializer

class NotificationDeliverySerializer(serializers.ModelSerializer):
    alert = AlertSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = NotificationDelivery
        fields = ['id', 'alert', 'user', 'channel', 'status', 'sent_at', 'error_message']
        read_only_fields = ['sent_at']