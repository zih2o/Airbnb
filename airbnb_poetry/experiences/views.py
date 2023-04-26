from django.utils import timezone
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import ParseError, PermissionDenied
from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from .serializers import (
    ExperienceDetailSerializer,
    ExperienceListSerializer,
    PerkSerializer,
    PublicBookingSerializer,
    CreateBookingSerializer,
)
from .models import Perk, Experience


class Experiences(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(
            experiences,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category does not exist")
            try:
                category = Category.objects.get(pk=category_pk)
                if category == Category.CategoryKindChoices.ROOMS:
                    raise ParseError(f"Category ID {category_pk} is not found")
            except Category.DoesNotExist:
                raise ParseError("Category is wrong")

            try:
                with transaction.atomic():
                    experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                    return Response(
                        ExperienceDetailSerializer(experience).data,
                    )
            except Exception:
                ParseError("Perk not found")
        else:
            return Response(serializer.errors)


class ExpericenDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(
            experience,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)

        if request.user != experience.host:
            raise PermissionDenied
        serializer = ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid:
            category_pk = request.data.get("category")
            if category_pk:
                category = Category.objects.get(category_pk)
                if category == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("Category is wrong")
            try:
                with transaction.atomic():
                    if category:
                        experience = serializer.save(category=category)
                    else:
                        experience = serializer.save()
                    perks = request.data.get("perks")
                    if perks:
                        experience.perks.clear()
                        for perk_pk in perks:
                            perk = Perk.objects.get(pk=perk_pk)
                            if perk:
                                experience.perks.add(perk)
                            else:
                                raise ParseError("Perk not found")
                    return Response(
                        ExperienceDetailSerializer(experience).data,
                    )
            except Exception:
                raise ParseError(Exception)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)

        if request.user != experience.host:
            raise PermissionDenied

        experience.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class ExperienceReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        experience = self.get_object(pk)
        page_size = 5
        start = (page - 1) * page_size
        end = start + page_size
        serializer = ReviewSerializer(
            experience.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                experience=self.get_object(pk),
            )
            return ReviewSerializer(review).data
        else:
            return Response(serializer.errors)


class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        experience = self.get_object(pk)
        page_size = 10
        start = page_size * (page - 1)
        end = start + page_size
        serializer = PerkSerializer(
            experience.perks.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class ExperiencePhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(experience=experience)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(serializer.errors)


class ExperienceBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
                experience=experience,
            )
            return Response(PublicBookingSerializer(booking).data)
        else:
            return Response(serializer.errors)


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
