from django.urls import path, include
from rest_framework.routers import DefaultRouter
from delivery.views import NotificationDeliveryViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationDeliveryViewSet, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
]