from urllib import request
from rest_framework import serializers
from .models import Amenity, Room
from medias.serializers import PhotoSerializer
from users.serializer import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        return room.owner == request.user


class RoomDetailSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(read_only=True)
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        return room.owner == request.user
