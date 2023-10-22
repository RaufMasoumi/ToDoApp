from django.shortcuts import reverse
from django.test import TestCase
from rest_framework import status
from .mixins import ViewBadUserTestsMixin
from .models import Task
# Create your tests here.

SHOULD_NOT_CONTAIN_TEXT = 'Hello I should not be in the template!'


class CustomTestCase(ViewBadUserTestsMixin, TestCase):
    pass


class TaskTests(CustomTestCase):
    def setUp(self):
        self.task = Task.objects.create(
            user=self.user,
            title='testtask'
        )
        self.task2 = Task.objects.create(
            user=self.user,
            title='testtask2'
        )

    def test_task_creation(self):
        self.assertEqual(Task.objects.count(), 2)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(task, self.task)
        self.assertEqual(task.title, self.task.title)
        self.assertFalse(task.is_done)

    def test_task_list_view(self):
        path = reverse('task-list')
        # bad user test
        content = [self.task.title, self.task2.title]
        self.login_required_and_user_itself_or_nothing_exists_test(path, should_not_contain_content=content)
        # correct user test
        self.client.force_login(self.user)
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for content in content:
            self.assertContains(response, content)
        self.assertNotContains(response, SHOULD_NOT_CONTAIN_TEXT)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.client.logout()

    def test_task_detail_view(self):
        path = reverse('task-detail', kwargs={'pk': self.task.pk})
        # absolute url test
        self.assertEqual(self.task.get_absolute_url(), path)
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.task.title)
        self.assertNotContains(response, self.task2.title)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.client.logout()

    def test_task_update_view(self):
        path = reverse('task-update', kwargs={'pk': self.task.pk})
        # absolute update url test
        self.assertEqual(self.task.get_absolute_update_url(), path)
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, 'Update')
        self.assertContains(get_response, self.task.title)
        self.assertNotContains(get_response, self.task2.title)
        self.assertTemplateUsed(get_response, 'tasks/task_update.html')
        # post
        data = {
            'title': 'updated'
        }
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(post_response, reverse('task-detail', kwargs={'pk': self.task.pk}))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, data['title'])
        self.client.logout()

    def test_task_delete_view(self):
        path = reverse('task-delete', kwargs={'pk': self.task.pk})
        # absolute delete url test
        self.assertEqual(self.task.get_absolute_delete_url(), path)
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, 'Delete')
        self.assertNotContains(get_response, SHOULD_NOT_CONTAIN_TEXT)
        self.assertTemplateUsed(get_response, 'tasks/task_delete.html')
        # post
        post_response = self.client.post(path)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(post_response, reverse('task-list'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.client.logout()


