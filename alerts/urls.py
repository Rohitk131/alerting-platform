from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alerts.views import AlertViewSet, UserAlertPreferenceViewSet

router = DefaultRouter()
router.register(r'', AlertViewSet, basename='alerts')
router.register(r'preferences', UserAlertPreferenceViewSet, basename='preferences')

urlpatterns = [
    path('', include(router.urls)),
]
