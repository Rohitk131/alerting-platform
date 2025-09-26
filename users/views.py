from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User, Team
from users.serializers import UserSerializer, TeamSerializer

class IsAdminPermission(permissions.BasePermission):
    """Custom permission to only allow admin users"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for managing teams"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAdminPermission]

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing users"""
    queryset = User.objects.select_related('team')
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """Admin permissions for create, update, delete"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminPermission()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return User.objects.select_related('team')
        return User.objects.filter(id=user.id).select_related('team')
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)