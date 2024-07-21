from django.urls import path
from apps.book.api.views import BookListAPIView, FilterBookListAPIView


urlpatterns = [
    path("", FilterBookListAPIView.as_view(), name="filter"),
    path("list/", BookListAPIView.as_view(), name="list"),
]
