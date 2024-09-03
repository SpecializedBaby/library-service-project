from django.utils import timezone

from rest_framework import serializers

from borrowing.models import Borrowing
from book.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer()

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
        read_only_fields = ("id", "borrow_date", "actual_return_date",)

    def validate(self, attrs):
        """
        Ensure that the book inventory is greater than 0 and the expected return date is after the borrow date.
        """

        book = attrs.get("book")

        if book.inventory <= 0:
            raise serializers.ValidationError("The selected book is not available in the inventory.")

        if attrs.get("expected_return_date") <= timezone.now():
            raise serializers.ValidationError("The expected return date must be in the future.")

        return attrs

    def create(self, validated_data):
        """
        Custom create method to decrease inventory and attach the current user.
        """

        book = validated_data["book"]
        book.inventory -= 1
        book.save()

        borrowing = Borrowing.objects.create(user=self.context["request"].user, **validated_data)

        return borrowing
