from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Account(TimeStampedModel):
    name = models.CharField(
        verbose_name=_("account name"), max_length=64, blank=False, null=False
    )
    type = models.CharField(
        verbose_name=_("account type"), max_length=12, blank=False, null=False
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
