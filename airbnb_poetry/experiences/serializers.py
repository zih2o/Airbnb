from rest_framework.serializers import ModelSerializer
from .models import Perk, Experience
from users.serializers import TinyUserSerializer


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


class ExperienceDetialSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)

    class Meta:
        model = Experience
        fields = "__all__"


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"
