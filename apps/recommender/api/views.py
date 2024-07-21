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
        try:
            data = Recommendation.suggest_genre(request.user.id)
            if not data:
                return Response({"message": "there is not enough data about you"},
                                status=status.HTTP_200_OK)

            serializer = self.serializer_class(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "unexpected error",
                             "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

