from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='teams', blank=True)

    def __str__(self):
        return self.name

class Alert(models.Model):

    SEVERITY_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]

    DELIVERY_TYPE_CHOICES = [
        ('in_app', 'In App'),
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=50, choices=SEVERITY_CHOICES)
    delivery_type = models.CharField(max_length=100, choices=DELIVERY_TYPE_CHOICES)
    start_time = models.DateTimeField(default=timezone.now)
    expiry_time = models.DateTimeField(null=True, blank=True)
    reminder_frequency = models.IntegerField(default=120)
    is_active = models.BooleanField(default=True)
    reminder_enabled = models.BooleanField(default=False)

    # visibility
    org_wide = models.BooleanField(default=False)
    teams = models.ManyToManyField(Team, blank=True, related_name='alerts')
    users = models.ManyToManyField(User, blank=True, related_name='alerts')

    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.severity}"
    
    def is_expired(self):
        if self.expiry_time:
            return timezone.now() > self.expiry_time
        return False

class NotificationDelivery(models.Model):
    STATUS_CHOICES = [
        ('delivered','delivered'),
        ('read','read'),
        ('unread','unread'),
    ]
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='deliveries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deliveries')
    delivered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='delivered')
    last_sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-delivered_at']

class UserAlertPreference(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alert_prefs')
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='user_prefs')
    read = models.BooleanField(default=False)
    snoozed_until = models.DateField(null=True, blank=True)  # date
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user','alert')