from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from wishlists.models import Wishlist
from medias.serializers import PhotoSerializer
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from bookings.models import Booking


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
            "kind",
            "icon_image",
            "pk",
        )


class RoomListSerializer(ModelSerializer):
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    is_liked = SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "name",
            "pk",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
            "is_liked",
            "owner",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user.pk,
            rooms__pk=room.pk,
        ).exists()


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(read_only=True)
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    is_liked = SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        if request:
            return room.owner == request.user
        return False

    def get_is_liked(self, room):
        request = self.context["request"]
        if request and request.user.is_authenticated:
            return Wishlist.objects.filter(
                user=request.user,
                rooms__pk=room.pk,
            ).exists()
        return []


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


class CreateBookingSerializer(ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("오늘 이전의 날짜에 예약할 수 없습니다.")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("오늘 이전의 날짜에 예약할 수 없습니다.")
        return value

    def validate(self, data):
        if data["check_in"] >= data["check_out"]:
            raise serializers.ValidationError("체크인 날짜는 체크아웃 날짜보다 빨라야 합니다.")
        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ):
            raise serializers.ValidationError("이미 예약된 날짜입니다.")

        return data
