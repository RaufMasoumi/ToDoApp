from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .mixins import ViewBadUserTestsMixin
from .models import TaskList
from .tests import SHOULD_NOT_CONTAIN_TEXT


class CustomAPITestCase(ViewBadUserTestsMixin, APITestCase):
    def login_required_test(self, path):
        # without authentication
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskListAPITests(CustomAPITestCase):

    def setUp(self):
        self.tasklist = TaskList.objects.create(
            user=self.user,
            title='testtasklist',
        )
        self.tasklist2 = TaskList.objects.create(
            user=self.user,
            title='testtasklist2'
        )

    def test_tasklist_lc_api_view(self):
        path = reverse('api-tasklist-list')
        # bad user test
        content = [self.tasklist.title, self.tasklist2.title]
        self.login_required_and_user_itself_or_nothing_exists_test(path, should_not_contain_content=content)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        for content in content:
            self.assertContains(get_response, content)
        self.assertNotContains(get_response, SHOULD_NOT_CONTAIN_TEXT)
        # post
        data = {
            'title': 'new tasklist'
        }
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TaskList.objects.filter(title=data['title']).exists())
        self.client.logout()

    def test_tasklist_rd_api_view(self):
        path = reverse('api-tasklist-detail', kwargs={'slug': self.tasklist.slug})
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.tasklist.title)
        self.assertNotContains(get_response, self.tasklist2.title)
        # delete
        delete_response = self.client.delete(path)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TaskList.objects.filter(pk=self.tasklist.pk).exists())
        self.client.logout()
