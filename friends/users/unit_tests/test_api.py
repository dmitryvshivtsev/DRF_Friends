import json
import os
from rest_framework.test import APITestCase, APIClient, RequestsClient
from rest_framework import status
from django.urls import reverse
from rest_framework.test import force_authenticate
from users.models import MyUser


class UsersAPITestCase(APITestCase):
    def test_status_code(self):
        user1 = MyUser.objects.create_user("test_user1", "Pas$w0rd")
        self.client.force_authenticate(user1)
        response = self.client.get("http://127.0.0.1:8000/api/v1/friends/all-users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_all_users(self):
        user2 = MyUser.objects.create_user("test_user2", "Pas$w0rd")
        user3 = MyUser.objects.create_user("test_user3", "Pas$w0rd")
        self.client.force_authenticate(user2)
        response = self.client.get("http://127.0.0.1:8000/api/v1/friends/all-users/")
        self.assertEqual(
            json.loads(response.content),
            {"all_users": [{"id": 2, "username": "test_user3"}]},
        )

    def test_status_of_user(self):
        user4 = MyUser.objects.create_user("test_user4", "Pas$w0rd")
        user5 = MyUser.objects.create_user("test_user5", "Pas$w0rd")
        self.client.force_authenticate(user4)
        response = self.client.get("http://127.0.0.1:8000/api/v1/friends/status/5/")
        self.assertEqual(
            response.data, {"id": 5, "username": "test_user5", "status": "Нет ничего"}
        )
