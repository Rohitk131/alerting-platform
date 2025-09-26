from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/alerts/', include('alerts.urls')),
    path('api/delivery/', include('delivery.urls')),
    path('api/', include('core.api_urls')),
]
