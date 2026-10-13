from datetime import date as Date
from decimal import Decimal, InvalidOperation

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Transaction
from .serializers import TransactionSerializer
from django.db.models import Count, Q, Sum
from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from decimal import Decimal
from django.contrib.admin.models import LogEntry
from rest_framework import serializers

@extend_schema(
    parameters=[
        OpenApiParameter("status", str, required=False),
        OpenApiParameter("date", str, required=False),
        OpenApiParameter("amount", float, required=False),
    ],
    responses=TransactionSerializer(many=True),
    tags=["transactions"]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_transactions(request):

    # Step 1: Get logged-in user's transactions
    transactions = Transaction.objects.filter(
        user=request.user
    ).select_related("card")

    # Step 2: Read optional filters
    status = request.query_params.get("status")
    date = request.query_params.get("date")
    amount = request.query_params.get("amount")

    # Step 3: Filter by payment status
    if status:
        status = status.upper()

        if status not in ["PENDING", "SUCCESS", "FAILED"]:
            return Response(
                {"error": "Invalid status"},
                status=400
            )

        transactions = transactions.filter(status=status)

    # Step 4: Filter by date
    if date:
        try:
            filter_date = Date.fromisoformat(date)
        except ValueError:
            return Response(
                {"error": "Date must be YYYY-MM-DD"},
                status=400
            )

        transactions = transactions.filter(
            created_at__date=filter_date
        )

    # Step 5: Filter by amount
    if amount is not None:
        try:
            filter_amount = Decimal(amount)
        except InvalidOperation:
            return Response(
                {"error": "Invalid amount"},
                status=400
            )

        transactions = transactions.filter(
            amount=filter_amount
        )

    # Step 6: Latest transactions first
    transactions = transactions.order_by("-created_at")

    # Step 7: Convert database records to JSON
    serializer = TransactionSerializer(
        transactions,
        many=True
    )

    return Response(serializer.data)


@extend_schema(tags=["admin"])
@api_view(["GET"])
@permission_classes([IsAdminUser])
def daily_payment_summary(request):

    # Get selected date or today's date
    selected_date = request.query_params.get("date")

    if not selected_date:
        selected_date = timezone.localdate().isoformat()

    # Get transactions for selected date
    payments = Transaction.objects.filter(
        created_at__date=selected_date
    )

    # Calculate summary
    summary = payments.aggregate(
        total_payments=Count("id"),

        pending_count=Count(
            "id",
            filter=Q(status="PENDING")
        ),

        success_count=Count(
            "id",
            filter=Q(status="SUCCESS")
        ),

        failed_count=Count(
            "id",
            filter=Q(status="FAILED")
        ),

        success_amount=Sum(
            "amount",
            filter=Q(status="SUCCESS")
        )
    )

    return Response({
        "date": selected_date,
        "total_payments": summary["total_payments"],
        "pending_count": summary["pending_count"],
        "success_count": summary["success_count"],
        "failed_count": summary["failed_count"],
        "success_amount": str(
            summary["success_amount"] or Decimal("0.00")
        )
    })


# Convert Django Admin log records into JSON
class AdminLogSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    action = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = [
            "id",
            "action_time",
            "username",
            "action",
            "object_repr",
            "change_message",
        ]

    def get_action(self, obj):
        return {
            1: "ADDITION",
            2: "CHANGE",
            3: "DELETION",
        }.get(obj.action_flag, "UNKNOWN")


# Admin Logs API
@extend_schema(
    responses=AdminLogSerializer(many=True),
    tags=["admin"]
)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_logs(request):

    logs = LogEntry.objects.select_related(
        "user"
    ).order_by("-action_time")[:100]

    serializer = AdminLogSerializer(
        logs,
        many=True
    )

    return Response(serializer.data)