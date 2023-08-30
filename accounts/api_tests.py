from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser


class CustomUserApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = CustomUser.objects.create_superuser(
            username='testsuperuser',
            password='testpass123'
        )
        cls.user1 = CustomUser.objects.create_user(
            username='testuser1',
            password='testpass1123'
        )
        cls.user2 = CustomUser.objects.create_user(
            username='testuser2',
            password='testpass2123'
        )

    def test_user_profile_retrieve_api_view(self):
        path = self.user1.get_absolute_api_url()
        # absolute api url test
        self.assertEqual(path, reverse('api-user-detail', kwargs={'slug': self.user1.slug}))
        # without authentication
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_403_FORBIDDEN)
        # with authentication but not valid user
        self.client.force_login(self.user2)
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
        # with authentication and admin
        self.client.force_login(self.superuser)
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user1.username)
        self.assertNotContains(response, self.user2.username)
        self.client.logout()
        # with authentication and user itself
        self.client.force_login(self.user1)
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        # with authentication but without passing kwargs
        self.client.force_login(self.user1)
        response = self.client.get(reverse('api-user-detail'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse('api-user-detail', kwargs={'slug': self.user1.slug}))
        self.client.logout()
