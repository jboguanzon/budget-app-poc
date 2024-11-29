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

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name
