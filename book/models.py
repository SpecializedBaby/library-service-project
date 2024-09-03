from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD", _("Hardcover")
        SOFT = "SOFT", _("Softcover")

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=4, choices=CoverChoices.choices, default=CoverChoices.SOFT)
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2, help_text=_("Daily fee in USD"))
    published_date = models.DateField()
    inventory = models.PositiveIntegerField()
    number_of_pages = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to="cover_image/", null=True, blank=True)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.title
