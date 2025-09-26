from rest_framework import viewsets, permissions
from delivery.models import NotificationDelivery
from delivery.serializers import NotificationDeliverySerializer

class IsAdminPermission(permissions.BasePermission):
    """Custom permission to only allow admin users"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class NotificationDeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing notification deliveries"""
    serializer_class = NotificationDeliverySerializer
    permission_classes = [IsAdminPermission]
    
    def get_queryset(self):
        return NotificationDelivery.objects.select_related('alert', 'user').order_by('-sent_at')
