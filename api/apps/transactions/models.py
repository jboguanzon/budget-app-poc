from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from apps.accounts.models import Account
from apps.categories.models import Category
from apps.payees.models import Payee


class Transaction(TimeStampedModel):
    account = models.ForeignKey(
        Account,
        verbose_name=_("account"),
        related_name="transactions",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(
        verbose_name=_("transaction date"),
        blank=False,
        null=False,
        default=timezone.now,
    )
    payee = models.ForeignKey(
        Payee,
        verbose_name=_("transaction payee"),
        related_name="transactions",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )
    notes = models.TextField(
        verbose_name=_("transaction notes"), blank=True, null=False, default=""
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_("transaction category"),
        related_name="transactions",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )
    amount = MoneyField(
        verbose_name=_("transaction amount"),
        max_digits=19,
        decimal_places=4,
        default_currency="PHP",
        blank=False,
        null=False,
        default=Money(0, "PHP"),
    )
    cleared = models.BooleanField(
        verbose_name=_("is transaction cleared?"),
        blank=False,
        null=False,
        default=False,
    )
    running_balance = MoneyField(
        verbose_name=_("transaction running balance"),
        max_digits=19,
        decimal_places=4,
        default_currency="PHP",
        blank=False,
        null=False,
        default=Money(0, "PHP"),
    )

    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")

    def __str__(self):
        return f"{self.account} - {self.date} - {self.payee} - {self.category} - {self.amount}"

    def get_previous_transactions(self):
        return Transaction.objects.filter(
            Q(account=self.account)
            & (
                Q(date__lt=self.date)
                | (Q(date__lte=self.date, created__lt=self.created))
            )
        ).order_by("-date", "-created")

    def get_previous_transaction(self):
        return self.get_previous_transactions().first()

    def get_subsequent_transactions(self):
        return Transaction.objects.filter(
            Q(account=self.account)
            & (
                Q(date__gt=self.date)
                | (Q(date__gte=self.date, created__gt=self.created))
            )
        ).order_by("date", "created")

    def get_previous_running_balance(self):
        previous_transaction = self.get_previous_transaction()
        return (
            previous_transaction.running_balance
            if previous_transaction
            else Money(0, self.amount.currency)
        )

    def recalculate_running_balances(self):
        with transaction.atomic():
            running_balance = self.get_previous_running_balance()
            running_balance += self.amount

            if self.running_balance != running_balance:
                Transaction.objects.filter(id=self.id).update(
                    running_balance=running_balance
                )

            subsequent_transactions = self.get_subsequent_transactions()
            for txn in subsequent_transactions:
                running_balance += txn.amount
                if txn.running_balance != running_balance:
                    Transaction.objects.filter(id=txn.id).update(
                        running_balance=running_balance
                    )
