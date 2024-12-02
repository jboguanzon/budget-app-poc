from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Payee(TimeStampedModel):
    name = models.CharField(
        verbose_name=_("payee"), max_length=64, blank=False, null=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("payee owner"),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("payee")
        verbose_name_plural = _("payees")

    def __str__(self):
        return self.name
