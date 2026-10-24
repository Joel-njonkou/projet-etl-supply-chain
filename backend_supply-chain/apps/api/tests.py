from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTests(APITestCase):
    def setUp(self):
        self.url = reverse("auth-register")
        self.payload = {
            "username": "jules-martin",
            "email": "jules@example.com",
            "password": "Correct-Horse-438-Lime",
            "password_confirmation": "Correct-Horse-438-Lime",
        }

    def test_registration_creates_regular_user_and_returns_jwt_tokens(self):
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        user = get_user_model().objects.get(username=self.payload["username"])
        self.assertTrue(user.check_password(self.payload["password"]))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_registration_rejects_mismatched_password_confirmation(self):
        response = self.client.post(
            self.url,
            {**self.payload, "password_confirmation": "Not-The-Same-438"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(username=self.payload["username"]).exists())

    def test_registration_rejects_weak_password(self):
        response = self.client.post(
            self.url,
            {**self.payload, "password": "password", "password_confirmation": "password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertFalse(get_user_model().objects.filter(username=self.payload["username"]).exists())

    def test_registration_rejects_duplicate_username(self):
        get_user_model().objects.create_user(username=self.payload["username"], password="Existing-Password-449!")

        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
