from django.contrib import admin
from .models import Experience, Perk


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """Experience Admin Model Definition"""

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "host",
        "start",
        "end",
        "category",
    )

    list_filter = (
        "category",
        "country",
        "city",
    )


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    """Perk Admin Model Definition"""

    list_display = (
        "name",
        "details",
        "description",
    )
