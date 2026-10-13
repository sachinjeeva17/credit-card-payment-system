from django.urls import path
from .views import view_transactions

urlpatterns = [
    path("", view_transactions),
    
]