from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT
from . import serializers
from .models import Perk, Experience


class Experiences(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experiences = Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(
            experiences,
            many=True,
        )
        return Response(serializer.data)

    # def post(self, request):
    #     serializer =


class Perks(APIView):
    def get(self, req):
        all_perk = Perk.objects.all()
        serializer = serializers.PerkSerializer(all_perk, many=True)
        return Response(serializer.data)

    def post(self, req):
        serializer = serializers.PerkSerializer(data=req.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(
                serializers.PerkSerializer(perk).data,
            )
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, req, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(
            perk,
            data=req.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(serializers.PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
