from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "daily_fee",
            "published_date",
            "inventory",
            "number_of_pages",
            "cover_image",
            "language",
        )
        read_only_fields = ("id",)


class BookDetailSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")
        read_only_fields = ("id",)
