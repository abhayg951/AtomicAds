from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Team, Alert
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = "Seed sample data users, teams and alerts"

    def handle(self, *args, **options):
        # Teams

        eng, _ = Team.objects.get_or_create(name="Engineering")
        mkt, _ = Team.objects.get_or_create(name="Marketing")

        # Users
        u1, _ = User.objects.get_or_create(username="alice", defaults={"email": "alice@example.com"})
        u2, _ = User.objects.get_or_create(username="bob", defaults={"email": "bob@example.com"})
        u3, _ = User.objects.get_or_create(username="charlie", defaults={"email": "charlie@example.com"})

        # Alerts
        a1, _ =Alert.objects.get_or_create(
            title='Database maintenance',
            message='We will have DB maintenance at midnight.',
            severity='warning',
            delivery_type='in_app',
            start_time=timezone.now() - timedelta(hours=1),
            expiry_time=timezone.now() + timedelta(days=7),
            org_wide=False,
        )

        a1.teams.add(eng)

        a2, _ = Alert.objects.get_or_create(
            title='Company All-hands',
            message='All hands tomorrow 10 AM',
            severity='info',
            delivery_type='in_app',
            start_time=timezone.now(),
            expiry_time=timezone.now() + timedelta(days=1),
            org_wide=True
        )

        self.stdout.write(self.style.SUCCESS("Seeded teams, users, and alerts."))