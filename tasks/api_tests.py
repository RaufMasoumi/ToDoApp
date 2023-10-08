from django.shortcuts import reverse
from rest_framework import status
from tasklists.tests import SHOULD_NOT_CONTAIN_TEXT
from tasklists.api_tests import CustomAPITestCase
from .models import Task


class TaskAPITests(CustomAPITestCase):
    def setUp(self):
        self.task = Task.objects.create(
            user=self.user,
            title='testtask',
        )
        self.task2 = Task.objects.create(
            user=self.user,
            title='testtask2',
        )

    def test_task_list_api_view(self):
        path = reverse('api-task-list')
        # bad user test
        content = [self.task.title, self.task2.title]
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
            'title': 'new task',
        }
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertTrue(Task.objects.filter(title=data['title']).exists())
        self.client.logout()

    def test_task_detail_api_view(self):
        path = reverse('api-task-detail', kwargs={'pk': self.task.pk})
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.task.title)
        self.assertNotContains(get_response, self.task2.title)
        # put
        data = {
            'title': 'updated',
        }
        put_response = self.client.put(path, data)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, data['title'])
        # delete
        delete_response = self.client.delete(path)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)
        self.assertFalse(Task.objects.filter(title=self.task.title).exists())
        self.client.logout()
