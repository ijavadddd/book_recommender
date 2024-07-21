from django.urls import path
from apps.recommender.api.views import (
    GenreRecommenderAPIView,
    UserBaseRecommenderAPIView,
)


urlpatterns = [
    path("", UserBaseRecommenderAPIView.as_view(), name="suggest"),
    path("genre/", GenreRecommenderAPIView.as_view(), name="suggest_genre"),
]
