from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from datetime import date


class HabitApiTests(APITestCase):
    def setUp(self):
        # Ensure DRF's APIClient is used (has .credentials())
        self.client = APIClient() 
        # Create two users
        self.u1 = User.objects.create_user(username="alice", email="a@a.com", password="Password123")
        self.u2 = User.objects.create_user(username="bob", email="b@b.com", password="Password123")

    def _login_and_set_auth(self, username: str, password: str) -> None:
        """Obtain JWT and set Authorization header on the test client."""
        resp = self.client.post(
            reverse("token_obtain_pair"),
            {"username": username, "password": password},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK, msg=f"Token obtain failed: {resp.content}")
        token = resp.json()["access"]  # use .json() for Pylance friendliness
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_registration(self):
        url = reverse("register")
        payload = {"username": "carol", "email": "c@c.com", "password": "Password123", "password2": "Password123"}
        r = self.client.post(url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_habit_visibility_and_permissions(self):
        # alice creates a habit
        self._login_and_set_auth("alice", "Password123")
        r_create = self.client.post(
            reverse("habit-list-create"),
            {"name": "Read", "period": "daily", "target": 1, "description": "", "tags": ""},
            format="json",
        )
        self.assertEqual(r_create.status_code, status.HTTP_201_CREATED)

        # bob cannot see alice's habit in his own list
        self._login_and_set_auth("bob", "Password123")
        r_list = self.client.get(reverse("habit-list-create"))
        self.assertEqual(r_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r_list.json()), 0)

    def test_log_crud_and_filter(self):
        # alice creates a habit
        self._login_and_set_auth("alice", "Password123")
        r_habit = self.client.post(
            reverse("habit-list-create"),
            {"name": "Walk", "period": "daily", "target": 1},
            format="json",
        )
        self.assertEqual(r_habit.status_code, status.HTTP_201_CREATED)
        habit_id = r_habit.json()["id"]

        # create two logs
        r_log1 = self.client.post(
            reverse("habitlog-list-create"),
            {"habit": habit_id, "count": 1, "noted_at": str(date(2025, 10, 10))},
            format="json",
        )
        self.assertEqual(r_log1.status_code, status.HTTP_201_CREATED)

        r_log2 = self.client.post(
            reverse("habitlog-list-create"),
            {"habit": habit_id, "count": 2, "noted_at": str(date(2025, 10, 11)), "note": "hilly"},
            format="json",
        )
        self.assertEqual(r_log2.status_code, status.HTTP_201_CREATED)

        # filter by date_to
        r_filter = self.client.get(reverse("habitlog-list-create") + "?date_to=2025-10-10")
        self.assertEqual(r_filter.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r_filter.json()), 1)

        # search by note
        r_search = self.client.get(reverse("habitlog-list-create") + "?search=hilly")
        self.assertEqual(r_search.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r_search.json()), 1)

        # update a log (owner can update)
        first_log_id = r_log1.json()["id"]
        r_update = self.client.patch(
            reverse("habitlog-detail", kwargs={"pk": first_log_id}),
            {"count": 5},
            format="json",
        )
        self.assertEqual(r_update.status_code, status.HTTP_200_OK)
        self.assertEqual(r_update.json()["count"], 5)
