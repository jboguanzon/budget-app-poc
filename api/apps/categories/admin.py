from django.contrib import admin

from .models import Category


class CategoryInline(admin.TabularInline):
    model = Category
    fields = ["name"]
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "user"]
    inlines = [CategoryInline]


admin.site.register(Category, CategoryAdmin)
