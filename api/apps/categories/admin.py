from django.contrib import admin

from .models import Category


class CategoryInline(admin.TabularInline):
    """Options for inline editing of subcategories."""

    model = Category
    fields = ["name"]
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    """Custom admin class for the Category model."""

    list_display = ["name", "parent", "user"]
    inlines = [CategoryInline]


admin.site.register(Category, CategoryAdmin)
