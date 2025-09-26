from django.apps import AppConfig

class DeliveryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'delivery'
    
    def ready(self):
        # Import tasks to ensure they are registered
        from delivery import tasks
