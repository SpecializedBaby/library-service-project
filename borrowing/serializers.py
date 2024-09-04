from django.utils import timezone

from rest_framework import serializers

from borrowing.models import Borrowing
from book.serializers import BookDetailSerializer


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )
        read_only_fields = (
            "id",
            "user",
            "borrow_date",
            "actual_return_date",
        )

    def validate(self, attrs):
        """
        Ensure that the book inventory is greater than 0 and the expected return date is after the borrow date.
        """

        book = attrs.get("book")

        if book.inventory <= 0:
            raise serializers.ValidationError(
                "The selected book is not available in the inventory."
            )

        if attrs.get("expected_return_date") <= timezone.now():
            raise serializers.ValidationError(
                "The expected return date must be in the future."
            )

        return attrs

    def create(self, validated_data):
        """
        Custom create method to decrease inventory and attach the current user.
        """

        book = validated_data.pop("book")
        book.inventory -= 1
        book.save()

        validated_data.pop("user", None)

        borrowing = Borrowing.objects.create(
            user=self.context["request"].user, book=book, **validated_data
        )

        return borrowing


class BorrowingListSerializer(BorrowingSerializer):
    book = BookDetailSerializer(read_only=True)


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date", )
        read_only_fields = ("id", )

    def validate(self, attrs):
        book = attrs.get("book")

        if self.instance.actual_return_date is not None:
            raise serializers.ValidationError("This borrowing has already been returned.")
        return attrs

    def save(self, **kwargs):
        borrowing = self.instance

        borrowing.actual_return_date = kwargs.get("actual_return_date")

        book = borrowing.book
        book.inventory += 1
        book.save()

        borrowing.save()
        return borrowing
