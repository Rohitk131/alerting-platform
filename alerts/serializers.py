from rest_framework import serializers
from alerts.models import Alert, UserAlertPreference
from users.serializers import TeamSerializer, UserSerializer

class AlertSerializer(serializers.ModelSerializer):
    visible_to_teams = TeamSerializer(many=True, read_only=True)
    visible_to_users = UserSerializer(many=True, read_only=True)
    visible_to_team_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    visible_to_user_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    is_expired = serializers.ReadOnlyField()
    is_current = serializers.ReadOnlyField()
    reminder_frequency_hours = serializers.SerializerMethodField()
    
    class Meta:
        model = Alert
        fields = [
            'id', 'title', 'message', 'severity', 'delivery_type', 'visibility_type',
            'visible_to_teams', 'visible_to_users', 'visible_to_team_ids', 'visible_to_user_ids',
            'start_time', 'expiry_time', 'reminder_frequency', 'reminder_frequency_hours', 
            'reminder_enabled', 'created_at', 'updated_at', 'is_active',
            'is_expired', 'is_current'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_reminder_frequency_hours(self, obj):
        return obj.reminder_frequency / 60  # Convert minutes to hours
    
    def create(self, validated_data):
        visible_to_team_ids = validated_data.pop('visible_to_team_ids', [])
        visible_to_user_ids = validated_data.pop('visible_to_user_ids', [])
        
        alert = Alert.objects.create(**validated_data)
        
        if visible_to_team_ids:
            from users.models import Team
            alert.visible_to_teams.set(Team.objects.filter(id__in=visible_to_team_ids))
        if visible_to_user_ids:
            from users.models import User
            alert.visible_to_users.set(User.objects.filter(id__in=visible_to_user_ids))
        
        return alert
    
    def update(self, instance, validated_data):
        visible_to_team_ids = validated_data.pop('visible_to_team_ids', None)
        visible_to_user_ids = validated_data.pop('visible_to_user_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if visible_to_team_ids is not None:
            from users.models import Team
            instance.visible_to_teams.set(Team.objects.filter(id__in=visible_to_team_ids))
        if visible_to_user_ids is not None:
            from users.models import User
            instance.visible_to_users.set(User.objects.filter(id__in=visible_to_user_ids))
        
        return instance

class UserAlertPreferenceSerializer(serializers.ModelSerializer):
    alert = AlertSerializer(read_only=True)
    is_snoozed = serializers.ReadOnlyField()
    
    class Meta:
        model = UserAlertPreference
        fields = [
            'id', 'alert', 'is_read', 'is_snoozed', 'snoozed_until',
            'last_reminder_sent_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'last_reminder_sent_at']
