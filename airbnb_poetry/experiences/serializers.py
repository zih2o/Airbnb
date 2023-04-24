from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from .models import Perk, Experience
from . import serializers
from users.serializers import TinyUserSerializer
from bookings.models import Booking


class ExperienceListSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "start",
            "end",
        )


class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)

    class Meta:
        model = Experience
        fields = "__all__"


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


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
