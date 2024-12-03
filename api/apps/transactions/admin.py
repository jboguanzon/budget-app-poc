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
        "running_balance",
        "cleared",
    ]
    readonly_fields = ["running_balance"]
