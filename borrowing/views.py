from rest_framework import generics, permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, mixins

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingListSerializer


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]

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

    def get_serializer_class(self):
        if self.action in ["list"]:
            self.serializer_class = BorrowingListSerializer
        else:
            self.serializer_class = BorrowingSerializer
        return super().get_serializer_class()
