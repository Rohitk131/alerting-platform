from django.urls import path
from core.views import AnalyticsViewSet

urlpatterns = [
    path('analytics/', AnalyticsViewSet.as_view({'get': 'dashboard'}), name='analytics-dashboard'),
]
