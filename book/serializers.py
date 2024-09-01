from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "published_date",
            "isbn_number",
            "number_of_pages",
            "cover_image",
            "language",
        )
        read_only_fields = ("id",)
