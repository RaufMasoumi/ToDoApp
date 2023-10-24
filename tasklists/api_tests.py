from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.api_tests import CustomAPITestCase
from tasks.tests import SHOULD_NOT_CONTAIN_TEXT
from tasks.models import Task
from .models import TaskList


class DefaultTaskListAPITests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.default_tasklist_permission = Permission.objects.get(codename='default_tasklist')

    def test_default_tasklist_permission(self):
        self.client.force_login(self.user)
        path = reverse('api-tasklist-detail', kwargs={'slug': self.user.tasklists.all_tasks().slug})
        # without permission
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        delete_response = self.client.delete(path)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
        # with permission
        self.user.user_permissions.add(self.default_tasklist_permission)
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        delete_response = self.client.delete(path)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()


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


class DefaultTasklistTasksAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.task = Task.objects.create(
            user=cls.user,
            title='testtask',
        )
        cls.default_tasklist_permission = Permission.objects.get(codename='default_tasklist')

    def test_task_default_tasklist_permission(self):
        self.client.force_login(self.user)
        path = reverse('api-tasklist-task-list', kwargs={'tasklist': self.user.tasklists.all_tasks().slug})
        # without permission
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        post_response = self.client.post(path)
        self.assertEqual(post_response.status_code, status.HTTP_403_FORBIDDEN)
        # with permission
        self.user.user_permissions.add(self.default_tasklist_permission)
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        post_response = self.client.post(path)
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()


class TaskListTaskAPITests(CustomAPITestCase):

    def setUp(self):
        self.tasklist = TaskList.objects.create(
            user=self.user,
            title='testtasklist',
        )
        self.task = Task.objects.create(
            user=self.user,
            title='testtask',
        )
        self.tasklist.tasks.add(self.task)

    def login_required_and_user_itself_or_somecode_test(self, path, method='delete', **kwargs):
        super().login_required_and_user_itself_or_somecode_test(path, method=method)

    def test_tasklist_task_lc_api_view(self):
        path = reverse('api-tasklist-task-list', kwargs={'tasklist': self.tasklist.slug})
        # bad user test
        content = [self.tasklist.title]
        self.login_required_and_user_itself_or_somecode_test(path)
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
            'title': 'new',
        }
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.tasklist.tasks.count(), 2)
        self.assertTrue(self.tasklist.tasks.filter(title=data['title']).exists())
        self.client.logout()

    def test_tasklist_task_destroy_api_view(self):
        path = reverse('api-tasklist-task-delete', kwargs={'tasklist': self.tasklist.slug, 'pk': self.task.pk})
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        delete_response = self.client.delete(path)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.tasklist.tasks.count(), 0)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        self.client.logout()
