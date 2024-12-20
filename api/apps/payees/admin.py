from django.contrib import admin

from .models import Payee


@admin.register(Payee)
class PayeeAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
