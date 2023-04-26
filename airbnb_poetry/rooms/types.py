import strawberry
from strawberry import auto
import typing
from . import models
from users.types import UserType
from reviews.types import ReviewType


@strawberry.django.type(models.Room)
class RoomType:
    id: auto
    name: auto
    kind: auto
    owner: "UserType"
    reviews: typing.List["ReviewType"]
