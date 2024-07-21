from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.book.api.serializers import BookSerializer
from apps.utils import StandardPagination
from apps.book.models import Book


class BookListAPIView(APIView):
    """
    List of all books.
    """

    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get(self, request):
        try:
            data = Book.list(user_id=request.user.id)
            serializer = self.serializer_class(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "unexpected error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FilterBookListAPIView(APIView):
    """
    filter books base on genre or author or title
    """

    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get(self, request):
        try:
            data = Book.list(dict(request.GET), request.user.id)
            serializer = self.serializer_class(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "unexpected error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
