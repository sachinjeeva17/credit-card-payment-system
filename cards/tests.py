from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


class CardTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="carduser",
            password="Test@12345Strong"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.card_data = {
            "cardholder_name": "Test User",
            "card_type": "CREDIT",
            "brand": "VISA",
            "last4": "1234",
            "expiry_month": 12,
            "expiry_year": 2030
        }

    def test_add_card(self):
        response = self.client.post(
            "/api/cards/add/",
            self.card_data
        )

        self.assertEqual(response.status_code, 201)

    def test_view_cards(self):
        self.client.post("/api/cards/add/", self.card_data)

        response = self.client.get("/api/cards/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_invalid_card(self):
        data = self.card_data.copy()
        data["last4"] = "12"

        response = self.client.post(
            "/api/cards/add/",
            data
        )

        self.assertEqual(response.status_code, 400)