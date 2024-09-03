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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["list"]:
            self.serializer_class = BorrowingListSerializer
        else:
            self.serializer_class = BorrowingSerializer
        return super().get_serializer_class()
