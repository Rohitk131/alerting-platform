from rest_framework import serializers
from users.models import User, Team

class TeamSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'created_at', 'member_count']
    
    def get_member_count(self, obj):
        return obj.members.count()

        
class UserSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    team_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'is_admin', 'team', 'team_id', 'date_joined'
        ]
        read_only_fields = ['date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        team_id = validated_data.pop('team_id', None)
        password = validated_data.pop('password', None)
        
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        
        if team_id:
            try:
                team = Team.objects.get(id=team_id)
                user.team = team
            except Team.DoesNotExist:
                pass
        
        user.save()
        return user