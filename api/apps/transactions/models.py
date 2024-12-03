from apps.accounts.models import Account
from apps.categories.models import Category
from apps.payees.models import Payee
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from djmoney.models.fields import MoneyField
from djmoney.money import Money


class Transaction(TimeStampedModel):
    class TypeChoices(models.TextChoices):
        INFLOW = "INFLOW", _("Inflow")
        OUTFLOW = "OUTFLOW", _("Outflow")

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
    type = models.CharField(
        verbose_name=_("transaction type"),
        max_length=12,
        choices=TypeChoices,
        blank=False,
        null=False,
        default=TypeChoices.INFLOW,
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

    def save(self, *args, **kwargs):
        # if not self.pk:
        #     self.amount.currency = self.account.currency

        running_balance = self.get_previous_running_balance()
        match self.type:
            case Transaction.TypeChoices.INFLOW:
                running_balance += self.amount
            case Transaction.TypeChoices.OUTFLOW:
                running_balance -= self.amount
            case _:
                raise Exception(f"Type {self.type} is not supported.")
        self.running_balance = running_balance

        super().save(*args, **kwargs)

    def get_previous_transaction(self):
        return (
            Transaction.objects.filter(account=self.account, date__lt=self.date)
            .order_by("-date", "-created")
            .first()
        )

    def get_previous_running_balance(self):
        previous_transaction = self.get_previous_transaction()
        return (
            previous_transaction.running_balance
            if previous_transaction
            # else Money(0, self.account.currency)
            else Money(0, self.amount.currency)
        )

    def recalculate_running_balances(self):
        with transaction.atomic():
            subsequent_transactions = (
                Transaction.objects.filter(account=self.account, date__gt=self.date)
                .order_by("date", "created")
                .select_for_update()
            )

            running_balance = self.get_previous_running_balance()
            match self.type:
                case Transaction.TypeChoices.INFLOW:
                    running_balance += self.amount
                case Transaction.TypeChoices.OUTFLOW:
                    running_balance -= self.amount
                case _:
                    raise Exception(f"Type {self.type} is not supported.")

            for txn in subsequent_transactions:
                match txn.type:
                    case Transaction.TypeChoices.INFLOW:
                        running_balance += txn.amount
                    case Transaction.TypeChoices.OUTFLOW:
                        running_balance -= txn.amount
                    case _:
                        raise Exception(f"Type {txn.type} is not supported.")

                if txn.running_balance != running_balance:
                    Transaction.objects.filter(id=txn.id).update(
                        running_balance=running_balance
                    )
