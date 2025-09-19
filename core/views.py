from django.db import models
from datetime import date
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Alert, Team, NotificationDelivery, UserAlertPreference
from .serializers import AlertSerializer, TeamSerializer, UserAlertPreferenceSerializer
from .services import trigger_reminder_for_alert
from django.contrib.auth import get_user_model

User = get_user_model()

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all().order_by('-created_at')
    serializer_class = AlertSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        severity = self.request.query_params.get('severity')
        status_param = self.request.query_params.get('status')
        if severity:
            qs = qs.filter(severity=severity)
        if status_param == 'active':
            qs = qs.filter(is_active=True, archived=False)
        elif status_param == 'expired':
            qs = qs.filter(expiry_time__lt=timezone.now(), archived=False)

        return qs
    
    @action(detail=True, methods=['post'])
    def trigger(self, request, pk=None):
        alert = self.get_object()
        summary = trigger_reminder_for_alert(alert)
        return Response(summary)

class UserAlertsViewSet(viewsets.ViewSet):

    def list(self, request, user_id=None):
        user = User.objects.get(pk=user_id)
        teams_ids = user.team_set.values_list('id', flat=True) if hasattr(user, 'team_set') else []
        alerts = Alert.objects.filter(is_active=True, archived=False).filter(
            models.Q(org_wide=True) |
            models.Q(users=user) |
            models.Q(teams__in=teams_ids)
        ).distinct()

        now = timezone.now()
        alerts = alerts.filter(models.Q(expiry_time__isnull=True) | models.Q(expiry_time__gt=now))
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def snooze(self, request, user_id=None, pk=None):
        user = User.objects.get(pk=user_id)
        alert = Alert.objects.get(pk=pk)
        today = date.today()
        pref, _ = UserAlertPreference.objects.get_or_create(user=user, alert=alert)
        pref.snoozed_until = today
        pref.save()
        
        return Response({'snoozed_until': str(pref.snoozed_until)})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, user_id=None, pk=None):
        user = User.objects.get(pk=user_id)
        alert = Alert.objects.get(pk=pk)

        pref, _ = UserAlertPreference.objects.get_or_create(user=user, alert=alert)
        pref.read = True
        pref.save()
        return Response({'read': pref.read})
    
    @action(detail=True, methods=['post'])
    def mark_unread(self, request, user_id=None, pk=None):
        user = User.objects.get(pk=user_id)
        alert = Alert.objects.get(pk=pk)

        pref, _ = UserAlertPreference.objects.get_or_create(user=user, alert=alert)
        pref.read = False
        pref.save()
        return Response({'read': pref.read})