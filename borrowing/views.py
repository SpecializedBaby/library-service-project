from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, mixins
from borrowing.helpers import send_telegram_message

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingListSerializer, BorrowingReturnSerializer


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    lookup_field = "id"

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")
        user = self.request.user
        queryset = self.queryset

        if user_id:
            user_id = self._params_to_ints(user_id)
            queryset = queryset.filter(user__id__in=user_id)

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)
        if not user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        borrowing = serializer.instance

        # Prepare the notification message
        message = (
            f"New Borrowing Created:\n\n"
            f"Book: {borrowing.book.title}\n"
            f"User: {borrowing.user.email}\n"
            f"Borrow Date: {borrowing.borrow_date}\n"
            f"Expected Return Date: {borrowing.expected_return_date}"
        )
        send_telegram_message(message)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.action in ["list"]:
            self.serializer_class = BorrowingListSerializer
        if self.action in ["update"]:
            self.serializer_class = BorrowingReturnSerializer
        else:
            self.serializer_class = BorrowingSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            raise ValidationError("This borrowing has already been returned.")

        borrowing.actual_return_date = timezone.now()

        book = borrowing.book
        book.inventory += 1
        book.save()

        borrowing.save()

        serializer = self.get_serializer(borrowing)

        return Response(serializer.data, status=status.HTTP_200_OK)
