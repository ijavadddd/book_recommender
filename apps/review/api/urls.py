from django.urls import path
from apps.review.api.views import (
    AddReviewAPIView,
    UpdateReviewAPIView,
    DeleteReviewAPIView,
)


urlpatterns = [
    path("add/", AddReviewAPIView.as_view(), name="add"),
    path("update/", UpdateReviewAPIView.as_view(), name="update"),
    path("delete/", DeleteReviewAPIView.as_view(), name="delete"),
]
