# proposals/utils_reminders.py
from datetime import date, timedelta
from django.db.models import Sum
from .models import Proposal, Payment

def get_user_reminders(user):
    today = date.today()
    proposal_alerts = []
    payment_alerts = []

    # === Proposal deadline reminders ===
    proposals = Proposal.objects.filter(user=user, status="Draft", last_date__isnull=False)
    for p in proposals:
        days_left = (p.last_date - today).days
        if days_left >= 0 and days_left <= 5:  # within 5 days
            proposal_alerts.append(f"Proposal #{p.id} deadline approaching in {days_left} days ({p.last_date}).")

    # === Payment reminders ===
    primary = Payment.objects.filter(proposal__user=user, is_primary=True)
    for prim in primary:
        received = Payment.objects.filter(proposal=prim.proposal, status="Received").aggregate(total=Sum("amount"))["total"] or 0
        balance = prim.amount - received
        if balance > 0 and prim.due_date:
            if prim.due_date < today:
                payment_alerts.append(f"Overdue payment of ${balance} (Proposal #{prim.proposal.id}, due {prim.due_date}).")
            elif prim.due_date == today:
                payment_alerts.append(f"Payment of ${balance} is due today (Proposal #{prim.proposal.id}).")

    return proposal_alerts, payment_alerts
