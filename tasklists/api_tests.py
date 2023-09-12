from rest_framework.test import APITestCase
from rest_framework import status
from .mixins import ViewBadUserTestsMixin


class CustomAPITestCase(ViewBadUserTestsMixin, APITestCase):
    def login_required_test(self, path):
        # without authentication
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_403_FORBIDDEN)
