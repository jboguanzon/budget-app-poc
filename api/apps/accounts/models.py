from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from djmoney.models.fields import CurrencyField
from djmoney.settings import CURRENCY_CHOICES


class Account(TimeStampedModel):
    name = models.CharField(
        verbose_name=_("account name"), max_length=64, blank=False, null=False
    )

    class AccountType(models.TextChoices):
        CREDIT = "CREDIT", _("Credit")
        DEBIT = "DEBIT", _("Debit")

    type = models.CharField(
        verbose_name=_("account type"),
        max_length=12,
        default=AccountType.DEBIT,
        blank=False,
        null=False,
        choices=AccountType,
    )

    currency = CurrencyField(
        verbose_name=_("account currency"),
        default="PHP",
        blank=False,
        null=False,
        choices=CURRENCY_CHOICES,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("account owner"),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    def __str__(self):
        return self.name
