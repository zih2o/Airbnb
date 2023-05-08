from django.conf import settings
import strawberry
from strawberry import auto
from strawberry.types import Info
import typing
from . import models
from users.types import UserType
from reviews.types import ReviewType
from wishlists.models import Wishlist


@strawberry.django.type(models.Amenity)
class AmenityType:
    id: auto
    name: auto
    description: auto


@strawberry.django.type(models.Room)
class RoomType:
    id: auto
    name: auto
    kind: auto
    country: auto
    city: auto
    price: auto
    rooms: auto
    toilets: auto
    description: auto
    address: auto
    pets_friendly: auto
    kind: auto
    category: auto
    amenities: typing.List["AmenityType"]
    owner: "UserType"

    @strawberry.field
    def reviews(
        self,
        page: typing.Optional[int] = 1,
    ) -> typing.List[ReviewType]:
        page_size = settings.PAGE_SIZE
        start = page + 1
        end = start + page_size
        return self.reviews.all()[start:end]

    @strawberry.field
    def rating(self) -> str:
        return self.rating()

    @strawberry.field
    def is_owner(self, info: Info) -> bool:
        return info.context.request.user == self.owner

    @strawberry.field
    def is_liked(self, info: Info) -> bool:
        return Wishlist.objects.filter(
            user=info.context.request.user,
            rooms__pk=self.pk,
        ).exists()
