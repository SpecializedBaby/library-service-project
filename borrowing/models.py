from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from book.models import Book


def validate_expected_return_date(value):
    """Validate that the expected return date is later than the borrow date."""
    if value < models.F("borrow_date"):
        raise ValidationError(
            _("Expected return date cannot be earlier than the borrow date.")
        )


class Borrowing(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    borrow_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.borrow_date is not None:
            """Custom validation logic to ensure date constraints."""
            if self.expected_return_date <= self.borrow_date:
                raise ValidationError(
                    {
                        "expected_return_date": _(
                            "Expected return date must be after borrow date."
                        )
                    }
                )
            if self.actual_return_date is not None and self.actual_return_date <= self.borrow_date:
                raise ValidationError(
                    {
                        "actual_return_date": _(
                            "Actual return date must be after borrow date."
                        )
                    }
                )

    def __str__(self):
        return f"{self.user} borrowed {self.book} on {self.borrow_date}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(expected_return_date__gt=models.F("borrow_date")),
                name="check_expected_return_date",
            ),
            models.CheckConstraint(
                check=models.Q(actual_return_date__gte=models.F("borrow_date"))
                | models.Q(actual_return_date__isnull=True),
                name="check_actual_return_date",
            ),
        ]
