from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status


class TaskListUserQuerysetMixin:
    request = None

    def get_queryset(self):
        return self.request.user.tasklists.all()


class DynamicTaskListTaskQuerysetMixin:
    request = None
    kwargs = None

    def get_tasklist(self):
        user_tasklists = self.request.user.tasklists.all()
        tasklist = get_object_or_404(user_tasklists, slug=self.kwargs.get('tasklist'))
        return tasklist

    def get_queryset(self):
        return self.get_tasklist().tasks.all()


def get_redirected_login_url(coming_from):
    return reverse('account_login') + f'?next={coming_from}'


class ViewBadUserTestsMixin:

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.bad_user = get_user_model().objects.create_user(
            username='testbaduser',
            password='testpass1123'
        )

    def get_bad_user(self):
        return getattr(self, 'bad_user', None)

    def login_required_test(self, path):
        # without authentication
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(no_response, get_redirected_login_url(path))

    def user_itself_or_somecode_test(self, path, bad_user=None, status_code=status.HTTP_404_NOT_FOUND):
        bad_user = bad_user or self.get_bad_user()
        # with authentication but not user itself
        self.client.force_login(bad_user)
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status_code)
        self.client.logout()

    def user_itself_or_200_but_nothing_exists_test(self, path, bad_user=None, should_not_contain_content=[]):
        bad_user = bad_user or self.get_bad_user()
        # with authentication but not user itself
        self.client.force_login(bad_user)
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_200_OK)
        for content in should_not_contain_content:
            self.assertNotContains(no_response, content)
        self.client.logout()

    def login_required_and_user_itself_or_somecode_test(self, path, bad_user=None, status_code=status.HTTP_404_NOT_FOUND):
        self.login_required_test(path)
        self.user_itself_or_somecode_test(path, bad_user, status_code)

    def login_required_and_user_itself_or_nothing_exists_test(self, path, bad_user=None, should_not_contain_content=None):
        self.login_required_test(path)
        self.user_itself_or_200_but_nothing_exists_test(path, bad_user, should_not_contain_content)

