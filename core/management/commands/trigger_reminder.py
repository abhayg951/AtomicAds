import json
from django.core.management.base import BaseCommand
from core.services import trigger_reminders_all
from django.utils import timezone

class Command(BaseCommand):
    help = "Trigger reminders for all alerts (simulate 2h cron)"

    def handle(self, *args, **options):
        now = timezone.now()
        results = trigger_reminders_all()
        self.stdout.write(self.style.SUCCESS(f"Triggered reminder at {now.isoformat()}"))
        self.stdout.write(json.dumps(results, indent=2, default=str))