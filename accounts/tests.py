from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


User = get_user_model()


class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser",
            password="Test@12345Strong"
        )

    def test_register(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "newuser",
                "password": "Test@12345Strong"
            }
        )

        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "testuser",
                "password": "Test@12345Strong"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_profile_without_login(self):
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, 401)

    def test_profile_with_login(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/auth/me/")

        self.assertEqual(response.status_code, 200)