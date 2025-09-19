from abc import ABC, abstractmethod
from django.utils import timezone
from datetime import date
from django.contrib.auth import get_user_model
from .models import Alert, NotificationDelivery, UserAlertPreference, Team
User = get_user_model()

class DeliveryStategy(ABC):
    @abstractmethod
    def deliver(self, alert, user):
        pass

class InAppDelivery(DeliveryStategy):

    def deliver(self, alert, user):
        nd, created = NotificationDelivery.objects.get_or_create(user=user, alert=alert)
        nd.status = 'delivered' if not nd.status =='read' else 'read'
        nd.last_sent_at = timezone.now()
        nd.save()
        return nd

class EmailDelivery(DeliveryStategy):

    def deliver(self, alert, user):
        nd, _ = NotificationDelivery.objects.get_or_create(user=user, alert=alert)
        nd.last_sent_at = timezone.now()
        nd.save()
        return nd

class SMSDelivery(DeliveryStategy):

    def deliver(self, alert, user):
        nd, _ = NotificationDelivery.objects.get_or_create(user=user, alert=alert)
        nd.last_sent_at = timezone.now()
        nd.save()
        return nd

STRATEGIES = {
    'in_app': InAppDelivery(),
    'email': EmailDelivery(),
    'sms': SMSDelivery(),
}

def get_relevant_users_for_alert(alert: Alert):
    if alert.org_wide:
        return User.objects.all()
    
    users = set()
    for u in alert.users.all():
        users.add(u)
    
    for team in alert.teams.all():
        for u in team.user_set.all():
            users.add(u)
    return list(users)

def should_send_to_user(user, alert: Alert):

    if alert.is_expired() or not alert.is_active or not alert.reminder_enabled:
        return False
    
    try:
        pref = UserAlertPreference.objects.get(user=user, alert=alert)
        if pref.snoozed_until:
            today = date.today()
            if pref.snoozed_until >= today:
                return False
    
    except UserAlertPreference.DoesNotExist:
        pass

    return True

def trigger_reminder_for_alert(alert: Alert):

    strategy = STRATEGIES.get(alert.delivery_type, STRATEGIES['in_app'])
    users = get_relevant_users_for_alert(alert)
    summary = {
        'delivered': 0,
        'skipped_snoozed': 0,
        'skipped_expired': 0    
        }
    
    for user in users:
        if should_send_to_user(user, alert):
            strategy.deliver(alert, user)
            summary['delivered'] += 1
        else:
            if alert.is_expired() or not alert.is_active or not alert.reminder_enabled:
                summary['skipped_expired'] += 1
            else:
                summary['skipped_snoozed'] += 1
    return summary

def trigger_reminders_all():

    results = {}
    alerts = Alert.objects.filter(is_active=True, archived=False, reminder_enabled=True)
    now = timezone.now()
    for alert in alerts:
        if alert.start_time and alert.start_time > now:
            continue
        if alert.expiry_time and alert.expiry_time < now:
            continue
        results[alert.id] = trigger_reminder_for_alert(alert)
    return results