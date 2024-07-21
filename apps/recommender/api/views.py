from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.book.api.serializers import BookSerializer
from apps.recommender.models import Recommendation
from rest_framework.response import Response
from rest_framework import status


class GenreRecommenderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        data = Recommendation.suggest_genre(request.user.id)
        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
