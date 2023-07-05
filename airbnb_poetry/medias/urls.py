from django.urls import path
from medias import views

urlpatterns = [
    path("photos/get-url", views.GetUploadUrl.as_view()),
    path("photos/<int:pk>", views.PhotoDetail.as_view()),
]
