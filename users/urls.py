from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, TeamViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='teams')
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
