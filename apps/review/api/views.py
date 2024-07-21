from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.review.api.serializers import (
    ReviewSerializer,
    DeleteReviewBookSerializer,
    BookSerializer,
)
from apps.review.models import Review


class AddReviewAPIView(APIView):
    """
    add review to book
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)

            if not serializer.is_valid():
                raise Exception(serializer.errors)

            validated_data = serializer.validated_data
            review = Review.count(
                {"book_id": validated_data["book_id"], "user_id": request.user.id}
            )
            if not review:
                add_review_data = Review.create(
                    {
                        "book_id": validated_data["book_id"],
                        "user_id": request.user.id,
                        "rating": validated_data["rating"],
                    },
                    request.user.id,
                )

                serializer = BookSerializer(data=add_review_data)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"message": "already submitted, try update or delete"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"message": "unexpected error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdateReviewAPIView(APIView):
    """
    update review to book
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)

            if not serializer.is_valid():
                raise Exception(serializer.errors)

            validated_data = serializer.validated_data
            review = Review.count(
                {"book_id": validated_data["book_id"], "user_id": request.user.id}
            )
            if review:
                add_review_data = Review.update(
                    {"rating": validated_data["rating"]},
                    {"book_id": validated_data["book_id"], "user_id": request.user.id},
                )

                serializer = BookSerializer(data=add_review_data)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"message": "no review found"}, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"message": "unexpected error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteReviewAPIView(APIView):
    """
    Delete review of book
    """

    serializer_class = DeleteReviewBookSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)

            if not serializer.is_valid():
                raise Exception(serializer.errors)

            validated_data = serializer.validated_data
            review = Review.count(
                {"book_id": validated_data["book_id"], "user_id": request.user.id}
            )

            if review:
                delete_review_result = Review.delete(
                    {"book_id": validated_data["book_id"], "user_id": request.user.id}
                )
                if delete_review_result:
                    return Response(
                        {"message": "review deleted successfully"},
                        status=status.HTTP_200_OK,
                    )
                raise Exception("review not deleted")
            return Response({"message": "no review found"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": "unexpected error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
