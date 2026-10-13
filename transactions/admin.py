import csv

from django.contrib import admin, messages
from django.http import HttpResponse
from django.db.models import Count, Sum, Q
from django.utils import timezone

from .models import Transaction
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

@admin.action(description="Export selected transactions to CSV")
def export_csv(modeladmin, request, queryset):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="transactions.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Reference",
        "Username",
        "Cardholder",
        "Brand",
        "Last 4",
        "Amount",
        "Currency",
        "Status",
        "Created At",
    ])

    for transaction in queryset.select_related("user", "card"):
        writer.writerow([
            transaction.reference,
            transaction.user.username,
            transaction.card.cardholder_name,
            transaction.card.brand,
            transaction.card.last4,
            transaction.amount,
            transaction.currency,
            transaction.status,
            transaction.created_at,
        ])
        # Record CSV export in Django Admin Logs
    LogEntry.objects.create(
        user=request.user,
        content_type=ContentType.objects.get_for_model(Transaction),
        object_repr="Transaction CSV Export",
        action_flag=CHANGE,
        change_message="Admin exported selected transactions to CSV"
    )
    return response


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "reference",
        "user",
        "card",
        "card_brand",
        "amount",
        "currency",
        "status",
        "created_at",
    ]

    list_filter = [
        "status",
        "created_at",
    ]

    search_fields = [
        "reference",
        "user__username",
        "card__last4",
    ]

    actions = [export_csv]

    readonly_fields = [
        "reference",
        "user",
        "card",
        "amount",
        "currency",
        "status",
        "failure_reason",
        "created_at",
    ]

    @admin.display(description="Brand")
    def card_brand(self, obj):
        return obj.card.brand

    def changelist_view(self, request, extra_context=None):

        today = timezone.localdate()

        summary = Transaction.objects.filter(
            created_at__date=today
        ).aggregate(
            total=Count("id"),
            success=Count("id", filter=Q(status="SUCCESS")),
            failed=Count("id", filter=Q(status="FAILED")),
            pending=Count("id", filter=Q(status="PENDING")),
            amount=Sum("amount", filter=Q(status="SUCCESS")),
        )

        messages.info(
            request,
            (
                f"Today's Payment Summary ({today}) | "
                f"Total: {summary['total']} | "
                f"Success: {summary['success']} | "
                f"Failed: {summary['failed']} | "
                f"Pending: {summary['pending']} | "
                f"Successful Amount: INR {summary['amount'] or 0}"
            )
        )

        return super().changelist_view(request, extra_context)