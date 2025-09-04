from django.db import transaction
from django.contrib.auth.models import User
from proposals.models import Profile, CreditTransaction

@transaction.atomic
def adjust_credits(user: User, delta: int, reason: str, *, method="other", note="", created_by=None) -> int:
    """
    Atomically adjust credits and create an audit log.
    Returns the new balance.
    """
    profile = Profile.objects.select_for_update().get(user=user)
    new_balance = profile.ai_credits + delta
    if new_balance < 0:
        raise ValueError("Insufficient credits for this operation.")

    profile.ai_credits = new_balance
    profile.save(update_fields=["ai_credits"])

    CreditTransaction.objects.create(
        user=user,
        delta=delta,
        reason=reason,
        method=method,
        note=note,
        balance_after=new_balance,
        created_by=created_by,
    )
    return new_balance
