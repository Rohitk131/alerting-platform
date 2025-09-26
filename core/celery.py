import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'send-reminders-every-2-hours': {
        'task': 'delivery.tasks.send_reminder_notifications',
        'schedule': crontab(minute=0, hour='*/2'),  # Every 2 hours
    },
    'cleanup-expired-alerts-daily': {
        'task': 'delivery.tasks.cleanup_expired_alerts',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
    },
}
app.conf.timezone = 'UTC'

app.autodiscover_tasks()