from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from alerts.models import Alert, UserAlertPreference
from alerts.serializers import AlertSerializer, UserAlertPreferenceSerializer
from delivery.services import NotificationService

class IsAdminPermission(permissions.BasePermission):
    """Custom permission to only allow admin users"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class AlertViewSet(viewsets.ModelViewSet):
    """ViewSet for managing alerts"""
    serializer_class = AlertSerializer
    
    def get_permissions(self):
        """Admin-only permissions for create, update, delete"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminPermission()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            # Admins see all alerts
            queryset = Alert.objects.all()
        else:
            # Regular users see only alerts targeted to them
            queryset = Alert.objects.filter(
                Q(visibility_type=Alert.VisibilityType.ORGANIZATION) |
                Q(visibility_type=Alert.VisibilityType.TEAM, visible_to_teams=user.team) |
                Q(visibility_type=Alert.VisibilityType.USER, visible_to_users=user),
                is_active=True
            ).distinct()
        
        # Filter by query parameters
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        
        status_filter = self.request.query_params.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(start_time__lte=timezone.now(), expiry_time__gt=timezone.now())
        elif status_filter == 'expired':
            queryset = queryset.filter(expiry_time__lt=timezone.now())
        
        return queryset.prefetch_related('visible_to_teams', 'visible_to_users')
    
    def perform_create(self, serializer):
        """Save alert and send initial notification"""
        alert = serializer.save()
        
        # Send initial notification
        notification_service = NotificationService()
        notification_service.send_alert(alert)
    
    @action(detail=True, methods=['post'])
    def send_now(self, request, pk=None):
        """Manually trigger alert sending"""
        if not request.user.is_admin:
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        alert = self.get_object()
        notification_service = NotificationService()
        deliveries = notification_service.send_alert(alert)
        
        return Response({
            'message': f'Alert sent to {len(deliveries)} users',
            'deliveries': len(deliveries)
        })

class UserAlertPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user alert preferences"""
    serializer_class = UserAlertPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAlertPreference.objects.filter(
            user=self.request.user
        ).select_related('alert', 'user')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark alert as read"""
        preference = self.get_object()
        preference.mark_read()
        return Response({'status': 'marked as read'})
    
    @action(detail=True, methods=['post'])
    def mark_unread(self, request, pk=None):
        """Mark alert as unread"""
        preference = self.get_object()
        preference.mark_unread()
        return Response({'status': 'marked as unread'})
    
    @action(detail=True, methods=['post'])
    def snooze(self, request, pk=None):
        """Snooze alert for the day"""
        preference = self.get_object()
        preference.snooze_for_day()
        return Response({
            'status': 'snoozed',
            'snoozed_until': preference.snoozed_until
        })
    
    @action(detail=True, methods=['post'])
    def unsnooze(self, request, pk=None):
        """Remove snooze from alert"""
        preference = self.get_object()
        preference.unsnooze()
        return Response({'status': 'unsnooze successful'})

