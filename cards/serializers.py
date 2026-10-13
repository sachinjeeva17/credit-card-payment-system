from datetime import date
from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):

    masked_number = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = [
            "id",
            "cardholder_name",
            "card_type",
            "brand",
            "masked_number",
            "last4",
            "expiry_month",
            "expiry_year",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "masked_number",
            "created_at",
        ]

    def get_masked_number(self, obj):
        return f"**** **** **** {obj.last4}"

    def validate_last4(self, value):
        if len(value) != 4 or not value.isdigit():
            raise serializers.ValidationError(
                "Last 4 digits must contain exactly 4 numbers"
            )
        return value

    def validate_expiry_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError(
                "Month must be between 1 and 12"
            )
        return value

    def validate(self, attrs):
        month = attrs["expiry_month"]
        year = attrs["expiry_year"]

        today = date.today()

        if (year, month) < (today.year, today.month):
            raise serializers.ValidationError(
                "Card has expired"
            )

        return attrs