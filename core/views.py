from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from alerts.models import Alert, UserAlertPreference
from delivery.models import NotificationDelivery

class AnalyticsViewSet(viewsets.ViewSet):
    """Analytics dashboard for alert metrics"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get system-wide analytics"""
        user = request.user
        
        if user.is_admin:
            # Admin gets full system analytics
            total_alerts = Alert.objects.count()
            active_alerts = Alert.objects.filter(is_current=True).count()
            expired_alerts = Alert.objects.filter(expiry_time__lt=timezone.now()).count()
            
            # Alert severity breakdown
            severity_breakdown = Alert.objects.values('severity').annotate(count=Count('id'))
            
            # Delivery statistics
            total_deliveries = NotificationDelivery.objects.count()
            delivered_count = NotificationDelivery.objects.filter(status=NotificationDelivery.Status.DELIVERED).count()
            failed_count = NotificationDelivery.objects.filter(status=NotificationDelivery.Status.FAILED).count()
            
            # Read vs Unread statistics
            read_count = UserAlertPreference.objects.filter(is_read=True).count()
            unread_count = UserAlertPreference.objects.filter(is_read=False).count()
            
            # Snooze statistics
            snoozed_count = UserAlertPreference.objects.filter(snoozed_until__gte=timezone.now().date()).count()
            
            # Per-alert statistics
            alert_stats = Alert.objects.annotate(
                total_recipients=Count('user_preferences'),
                read_count=Count('user_preferences', filter=Q(user_preferences__is_read=True)),
                snoozed_count=Count('user_preferences', filter=Q(user_preferences__snoozed_until__gte=timezone.now().date()))
            ).values('id', 'title', 'severity', 'total_recipients', 'read_count', 'snoozed_count')
            
            analytics_data = {
                'total_alerts': total_alerts,
                'active_alerts': active_alerts,
                'expired_alerts': expired_alerts,
                'severity_breakdown': list(severity_breakdown),
                'delivery_stats': {
                    'total_delivered': total_deliveries,
                    'successful_deliveries': delivered_count,
                    'failed_deliveries': failed_count,
                    'delivery_rate': (delivered_count / total_deliveries * 100) if total_deliveries > 0 else 0
                },
                'engagement_stats': {
                    'total_read': read_count,
                    'total_unread': unread_count,
                    'read_rate': (read_count / (read_count + unread_count) * 100) if (read_count + unread_count) > 0 else 0
                },
                'snooze_stats': {
                    'total_snoozed': snoozed_count
                },
                'alert_details': list(alert_stats)
            }
        else:
            # Regular users get limited analytics about their own alerts
            user_preferences = UserAlertPreference.objects.filter(user=user)
            
            total_user_alerts = user_preferences.count()
            read_alerts = user_preferences.filter(is_read=True).count()
            unread_alerts = user_preferences.filter(is_read=False).count()
            snoozed_alerts = user_preferences.filter(snoozed_until__gte=timezone.now().date()).count()
            
            analytics_data = {
                'user_alert_stats': {
                    'total_alerts': total_user_alerts,
                    'read_alerts': read_alerts,
                    'unread_alerts': unread_alerts,
                    'snoozed_alerts': snoozed_alerts,
                    'read_rate': (read_alerts / total_user_alerts * 100) if total_user_alerts > 0 else 0
                }
            }
        
        return Response(analytics_data)