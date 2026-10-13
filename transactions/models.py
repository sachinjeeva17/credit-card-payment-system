import uuid

from django.db import models
from django.conf import settings


def generate_reference():
    return f"PAY-{uuid.uuid4().hex[:12].upper()}"


class Transaction(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    reference = models.CharField(
        max_length=30,
        unique=True,
        default=generate_reference,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    card = models.ForeignKey(
        "cards.Card",
        on_delete=models.PROTECT
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=3,
        default="INR"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    failure_reason = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference