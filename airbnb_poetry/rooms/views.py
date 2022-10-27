from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT

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
                    raise ParseError
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError
                except Category.DoesNotExist:
                    raise ParseError
                room = serializer.save(
                    owner=req.user,
                    category=category,
                )
                return Response(RoomDetailSerializer(room).data)
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
