# proposals/management/commands/send_daily_reminders.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from proposals.utils_reminders import get_user_reminders
from proposals.utils_email import send_user_email

User = get_user_model()

class Command(BaseCommand):
    help = "Send daily email reminders to users"

    def handle(self, *args, **options):
        for user in User.objects.all():
            if not user.email:
                continue
            proposal_alerts, payment_alerts = get_user_reminders(user)
            if not proposal_alerts and not payment_alerts:
                body = "Hi, no pending dues and no deadlines missed today. 🎉"
            else:
                body = "Hi, here are your reminders:\n\n"
                for a in proposal_alerts:
                    body += f"- {a}\n"
                for a in payment_alerts:
                    body += f"- {a}\n"

            send_user_email(user, "Your JRP Daily Reminders", body)
            self.stdout.write(self.style.SUCCESS(f"Sent reminders to {user.username}"))
