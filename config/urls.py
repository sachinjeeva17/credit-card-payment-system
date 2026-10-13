from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from transactions.views import daily_payment_summary,admin_logs
urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/", include("accounts.urls")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/cards/", include("cards.urls")),
    path("api/transactions/", include("transactions.urls")),
    path(
    "api/admin/daily-summary/",
    daily_payment_summary,
    name="admin-daily-summary"
),
    path(
    "api/admin/logs/",
    admin_logs,
    name="admin-logs"
),
]