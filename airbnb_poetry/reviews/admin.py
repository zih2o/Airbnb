from django.contrib import admin
from .models import Review


class rating_filter(admin.SimpleListFilter):
    title = "Filter by Rating"
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return [
            ("good", "좋은 리뷰 (3점 이상)"),
            ("bad", "나쁜 리뷰 (3점 미만)"),
        ]

    def queryset(self, request, reviews):
        rating = self.value()
        if rating == "good":
            return reviews.filter(rating__gte=3)
        elif rating == "bad":
            return reviews.filter(rating__lt=3)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    """Review Admin Model"""

    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (rating_filter,)
