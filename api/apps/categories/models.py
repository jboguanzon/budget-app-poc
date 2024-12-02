from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(
        verbose_name=_("category name"), max_length=64, blank=False, null=False
    )
    parent = models.ForeignKey(
        "self",
        verbose_name=_("parent category"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="subcategories",
        related_query_name="subcategories",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("category owner"),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name
