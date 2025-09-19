from django.contrib import admin
from .models import Alert, UserAlertPreference, NotificationDelivery, Team

# Register your models here.

admin.site.register(Alert)
admin.site.register(UserAlertPreference)
admin.site.register(NotificationDelivery)
admin.site.register(Team)