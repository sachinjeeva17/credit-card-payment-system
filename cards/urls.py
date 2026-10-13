from django.urls import path
from .views import add_card, view_cards, delete_card,get_card_by_id


urlpatterns = [
    path("add/", add_card),
    path("", view_cards),
    path("<int:card_id>/", get_card_by_id, name="get_card_by_id"),
    path("<int:card_id>/", delete_card),
]