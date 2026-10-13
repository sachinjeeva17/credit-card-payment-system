from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    cardholder_name = serializers.CharField(
        source="card.cardholder_name",
        read_only=True
    )

    brand = serializers.CharField(
        source="card.brand",
        read_only=True
    )

    card_type = serializers.CharField(
        source="card.card_type",
        read_only=True
    )

    masked_number = serializers.SerializerMethodField()

    last4 = serializers.CharField(
        source="card.last4",
        read_only=True
    )

    expiry_month = serializers.IntegerField(
        source="card.expiry_month",
        read_only=True
    )

    expiry_year = serializers.IntegerField(
        source="card.expiry_year",
        read_only=True
    )

    class Meta:
        model = Transaction

        fields = [
            "id",
            "reference",
            "cardholder_name",
            "brand",
            "card_type",
            "masked_number",
            "last4",
            "expiry_month",
            "expiry_year",
            "amount",
            "currency",
            "status",
            "failure_reason",
            "created_at",
        ]

    def get_masked_number(self, obj):
        return f"**** **** **** {obj.card.last4}"