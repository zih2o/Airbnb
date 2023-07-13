from django.db import models
from common.models import CommonModel
import base64


class Room(CommonModel):

    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = "entire_place", "Entire_Place"
        PRIVATE_ROOM = "private_room", "Private_Room"
        SHARED_ROOM = "shared_room", "Shared_Room"

    name = models.CharField(max_length=80, default="")

    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pets_friendly = models.BooleanField(default=False)
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        blank=True,
        related_name="rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )

    def __str__(self):
        return self.name

    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return "No Reviews"
        total = 0
        for rating in self.reviews.all().values("rating"):
            total += rating["rating"]
        return round(total / count, 1)


class Amenity(CommonModel):

    """Amenity model Definition"""

    class AmenityKindChoices(models.TextChoices):
        VIEW = "view", "전망"
        BATH_ROOM = "bath_room", "욕실"
        BED_ROOM_AND_LAUNDRY = "bed_room_and_laundry", "침실 및 세탁 시설"
        ENTERTAINMENT = "entertainment", "엔터테인먼트"
        AIR_CONDITIONING = "air_conditioning", "냉난방"
        SAFETY = "safety", "숙소 안전"
        WORK_SPACE = "work_space", "인터넷 및 작업 공간"
        KICHEN_AND_DINING = "kichen_and_dining", "주방 및 식당"
        LOCATION = "location", "위치 특성"
        PARK_AND_ETC = "park_and_etc", "주차장 및 기타 시설"
        SERVICE = "service", "서비스"

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, blank=True, null=True)
    kind = models.CharField(
        choices=AmenityKindChoices.choices, max_length=100, null=True
    )

    icon_image = models.TextField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
