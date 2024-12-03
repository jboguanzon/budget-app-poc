from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "account",
        "date",
        "payee",
        "category",
        "amount",
        "type",
        "running_balance",
        "cleared",
    ]
