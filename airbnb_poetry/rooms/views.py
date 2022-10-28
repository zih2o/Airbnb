from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from django.db import transaction

from categories.models import Category
from .serializer import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from .models import Amenity, Room
from rooms import serializer


class Amenities(APIView):
    def get(self, request):
        all_amenity = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenity,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_data = serializer.save()
            return Response(AmenitySerializer(updated_data).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, req):
        all_room = Room.objects.all()
        serializer = RoomListSerializer(all_room, many=True)
        return Response(serializer.data)

    def post(self, req):
        if req.user.is_authenticated():
            serializer = RoomDetailSerializer(data=req.data)
            if serializer.is_valid():
                category_pk = req.data.get("category")
                if not category_pk:
                    raise ParseError("Category does not exist")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError(f"Category ID {category_pk} is not found")
                except Category.DoesNotExist:
                    raise ParseError("Category is wrong")

                try:
                    with transaction.atomic():
                        room = serializer.save(
                            owner=req.user,
                            category=category,
                        )
                        amenities = req.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        return Response(RoomDetailSerializer(room).data)

                except Exception:
                    ParseError("Amenity not found")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, req, pk):

        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated():
            raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                category = Category.objects.get(category_pk)
                if category == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("Category is wrong")
        try:
            with transaction.atomic():
                if category:
                    room = serializer.save(category=category)
                else:
                    room = serializer.save()
                amenities = request.data.get("amenities")
                if amenities:
                    room.amenities.clear()
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        if amenity:
                            room.amenities.add(amenity)
                        else:
                            raise ParseError("Amenity not found")
                return Response(RoomDetailSerializer(room).data)

        except Exception:
            raise ParseError(Exception)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated():
            raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        room.delete()

        return Response(status=HTTP_204_NO_CONTENT)
