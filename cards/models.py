from django.db import models
from django.conf import settings


class Card(models.Model):

    CARD_TYPES = [
        ("CREDIT", "Credit"),
        ("DEBIT", "Debit"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    cardholder_name = models.CharField(max_length=100)

    card_type = models.CharField(
        max_length=10,
        choices=CARD_TYPES
    )

    brand = models.CharField(max_length=30)

    last4 = models.CharField(max_length=4)

    expiry_month = models.IntegerField()

    expiry_year = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} - {self.last4}"