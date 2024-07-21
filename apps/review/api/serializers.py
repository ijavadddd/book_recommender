from rest_framework import serializers
from apps.book.api.serializers import BookSerializer
from apps.book.models import Book


class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField(max_value=5, min_value=1)

    def get_book(self, obj):
        book = Book.get_dict(obj["book_id"])
        serializer_instance = BookSerializer(data=book)
        serializer_instance.is_valid(raise_exception=True)
        return serializer_instance.data


class DeleteReviewBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(write_only=True)
