from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from tasks.tests import CustomTestCase, SHOULD_NOT_CONTAIN_TEXT
from .models import CustomUser
# Create your tests here.


class CustomUserTests(CustomTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser = CustomUser.objects.create_superuser(
            username='testsuperuser',
            password='testpass123'
        )
        cls.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass1123'
        )

    def test_custom_user_activation(self):
        self.assertEqual(get_user_model(), CustomUser)

    def test_custom_user_model(self):
        self.assertEqual(CustomUser.objects.count(), 2)
        superuser = CustomUser.objects.get(is_superuser=True)
        user = CustomUser.objects.get(is_superuser=False)
        self.assertEqual(superuser, self.superuser)
        self.assertEqual(superuser.username, self.superuser.username)
        self.assertEqual(user, self.user)
        self.assertEqual(user.username, self.user.username)

    def test_user_slug_auto_creation(self):
        self.assertEqual(self.user.slug, 'testuser')

    def test_user_profile_view(self):
        path = reverse('user-detail', kwargs={'slug': self.user.slug})
        # absolute url test
        self.assertEqual(self.user.get_absolute_url(), path)
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path, bad_user=self.superuser,
                                                             status_code=status.HTTP_403_FORBIDDEN)
        # correct user test
        self.client.force_login(self.user)
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'accounts/user_detail.html')
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, SHOULD_NOT_CONTAIN_TEXT)
        # without passing kwargs
        response_without_kw = self.client.get(reverse('user-detail'))
        self.assertEqual(response_without_kw.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response_without_kw, reverse('user-detail', kwargs={'slug': self.user.slug}))
        self.client.logout()
