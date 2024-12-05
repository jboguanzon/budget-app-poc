from django.contrib import admin

from .models import Payee


@admin.register(Payee)
class PayeeAdmin(admin.ModelAdmin):
    """Custom admin class for the Payee model."""

    list_display = ["name", "user"]
