from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Custom admin class for the Account model."""

    list_display = ["name", "type", "currency", "user"]
