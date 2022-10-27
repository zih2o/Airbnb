from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from .serializer import PerkSerializer
from .models import Perk


class Perks(APIView):
    def get(self, req):
        all_perk = Perk.objects.all()
        serializer = PerkSerializer(all_perk, many=True)
        return Response(serializer.data)

    def post(self, req):
        serializer = PerkSerializer(data=req.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(
                PerkSerializer(perk).data,
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
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, req, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(
            perk,
            data=req.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
