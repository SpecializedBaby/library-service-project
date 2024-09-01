from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn_number = models.CharField(max_length=13, unique=True)
    number_of_pages = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to="cover_image/", null=True, blank=True)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.title
