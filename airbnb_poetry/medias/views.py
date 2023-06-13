from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Photo


class PhotoDetail(APIView):
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        permission_classes = [IsAuthenticated]

        photo = self.get_object(pk)
        if (photo.room and request.user != photo.room.owner) or (
            photo.experience and request.user != photo.experience.host
        ):
            raise PermissionDenied
        else:
            photo.delete()
            return Response(status=HTTP_204_NO_CONTENT)
