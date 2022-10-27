from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    """Category Model Admin"""

    list_display = (
        "name",
        "kind",
    )

    list_filter = ("kind",)
