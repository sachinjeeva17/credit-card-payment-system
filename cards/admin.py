from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "user",
        "cardholder_name",
        "card_type",
        "brand",
        "last4",
        "expiry_month",
        "expiry_year",
    ]

    list_filter = ["card_type", "brand"]

    search_fields = ["cardholder_name", "last4"]