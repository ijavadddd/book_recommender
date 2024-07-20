from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.book.api.serializers import BookSerializer
from django.db import connection
from apps.utils import StandardPagination


class BookListAPIView(APIView):
    """
    List of all books.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get(self, request):
        query = "SELECT * FROM books ORDER BY title;"

        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Open a cursor to perform database operations
            with connection.cursor() as cursor:
                cursor.execute(query)
                # get column name to convert tuple to dic for easy serialization
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

                serializer = self.serializer_class(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "unexpected error",
                             "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilterBookListAPIView(APIView):
    """
    List of all books.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get(self, request):
        # Convert QueryDict to a regular dictionary if needed
        query_dict = dict(request.GET)
        query_filter = ""
        if query_dict:
            query_filter = "WHERE " + " AND ".join([f"{key} LIKE '{value[0]}'" for key, value in query_dict.items()])

        query = f"SELECT * FROM books {query_filter} ORDER BY title;"

        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Open a cursor to perform database operations
            with connection.cursor() as cursor:
                cursor.execute(query)
                # get column name to convert tuple to dic for easy serialization
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

                serializer = self.serializer_class(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "unexpected error",
                             "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
