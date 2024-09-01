from django.shortcuts import render
from django.views import generic
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ["list"]:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAdminUser, ]

        return super().get_permissions()
