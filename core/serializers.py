from rest_framework import serializers
from .models import Alert, Team, UserAlertPreference
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']

class AlertSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)
    team_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Team.objects.all(), source='teams')
    user_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=User.objects.all(), source='users')

    class Meta:
        model = Alert
        fields = [
            'id',
            'title',
            'message',
            'severity',
            'delivery_type',
            'start_time',
            'expiry_time',
            'reminder_frequency_minutes',
            'is_active',
            'reminder_enabled',
            'org_wide',
            'teams',
            'team_ids',
            'user_ids',
            'created_at',
            'archived'
    ]

class UserAlertPreferenceSerializer(serializers.ModelSerializer):
    alert = serializers.PrimaryKeyRelatedField(queryset=Alert.objects.all())
    class Meta:
        model = UserAlertPreference
        fields = ['id','user','alert','read','snoozed_until','updated_at']
        read_only_fields = ['updated_at']
