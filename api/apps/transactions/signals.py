from django.db.models import signals
from django.dispatch import receiver

from .models import Transaction


@receiver(signals.post_save, sender=Transaction)
def recalculate_running_balances(sender, instance, created, **kwargs):
    """Signal handler to recalculate running balances when a transaction is modified"""
    if not kwargs.get("raw", False):  # Skip during fixtures/migrations
        instance.recalculate_running_balances()
