from django.db import models
from common.models import CommonModel
from experiences.models import Experience


class Booking(CommonModel):

    """Booking for a room or an exprience"""

    class BookingKindChoices(models.TextChoices):

        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"

    kind = models.CharField(
        max_length=20,
        choices=BookingKindChoices.choices,
    )
    user = models.ForeignKey(
        "users.user",
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookings",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookings",
    )
    check_in = models.DateField(
        null=True,
        blank=True,
    )
    check_out = models.DateField(
        null=True,
        blank=True,
    )
    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    guests = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.kind.title()} booking for : {self.user}"
