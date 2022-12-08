from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_200_OK
from .serializer import WishlistSerializer
from .models import Wishlist
from rooms.models import Room

class Wishlists(APIView):
    
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlists,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            return Response(WishlistSerializer(wishlist).data)
        else:
            return Response(serializer.errors)
    
class WishlistDetail(APIView):
    
    permission_classes=[IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            wishlist = Wishlist.objects.get(pk=pk, user=user)
            return wishlist
        except Wishlist.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serialzer = WishlistSerializer(wishlist, context={"request": request},)
        return Response(serialzer.data)
    
    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user, )
        serializer = WishlistSerializer(wishlist, data=request.data, partial=True,context={"request": request},)
        if serializer.is_valid():
            wishlist = serializer.save()
            return Response(WishlistSerializer(wishlist, context={"request": request},).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(HTTP_200_OK)
        
class WishlistRoom(APIView):
    
    permission_classes=[IsAuthenticated]
    
    def get_list(self, pk, user):
        try:
            wishlist = Wishlist.objects.get(pk=pk, user=user)
            return wishlist
        except Wishlist.DoesNotExist:
            raise NotFound
    
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            raise NotFound
        
    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(HTTP_200_OK)