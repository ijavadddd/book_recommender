from django.urls import path
from apps.recommender.api.views import GenreRecommenderAPIView


urlpatterns = [
    path('', GenreRecommenderAPIView.as_view(), name='suggest'),
]
