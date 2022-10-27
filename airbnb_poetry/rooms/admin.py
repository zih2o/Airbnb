from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)
    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "rating",
        "total_amenities",
        "created_at",
        "updated_at",
        "category",
    )
    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pets_friendly",
        "kind",
        "amenities",
        "category",
    )

    search_fields = ("name",)

    def total_amenities(self, room):
        return room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
