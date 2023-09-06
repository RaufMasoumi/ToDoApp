from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils import timezone
from rest_framework import status
from tasks.models import Task
from .models import TaskList
# Create your tests here.

SHOULD_NOT_CONTAIN_TEXT = 'Hello I should not be in the template!'


def get_redirected_login_url(coming_from):
    return reverse('account_login') + f'?next={coming_from}'


class TaskListTests(TestCase):

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

    def setUp(self):
        self.tasklist = TaskList.objects.create(
            user=self.user,
            title='testtasklist',
        )
        self.tasklist2 = TaskList.objects.create(
            user=self.user,
            title='testtasklist2',
        )
        self.task = Task.objects.create(
            user=self.user,
            title='testtask',
        )
        self.tasklist.tasks.add(self.task)

    def test_tasklist_model(self):
        self.assertEqual(TaskList.objects.count(), 2)
        tasklist = TaskList.objects.get(pk=self.tasklist.pk)
        self.assertEqual(tasklist, self.tasklist)
        self.assertEqual(tasklist.title, 'testtasklist')

    def test_tasklist_slug_auto_creation(self):
        self.assertEqual(self.tasklist.slug, 'testtasklist')

    def test_tasklist_list_view(self):
        path = reverse('tasklist-list')
        # without authentication
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(no_response, get_redirected_login_url(path))
        # with authentication but not user itself
        self.client.force_login(self.bad_user)
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_200_OK)
        self.assertNotContains(no_response, self.tasklist.title)
        self.client.logout()
        # with authentication and user itself
        self.client.force_login(self.user)
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context.get('tasklists')), 2)
        self.assertContains(response, self.tasklist.title)
        self.assertContains(response, self.tasklist2.title)
        self.assertNotContains(response, SHOULD_NOT_CONTAIN_TEXT)
        self.assertTemplateUsed(response, 'tasklists/tasklist_list.html')

    def test_tasklist_detail_view(self):
        path = reverse('tasklist-detail', kwargs={'slug': self.tasklist.slug})
        # absolute url test
        self.assertEqual(self.tasklist.get_absolute_url(), path)
        # without authentication
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(no_response, get_redirected_login_url(path))
        # with authentication but not user itself
        self.client.force_login(self.bad_user)
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
        # with authentication and user itself
        self.client.force_login(self.user)
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'tasklists/tasklist_detail.html')
        self.assertContains(response, self.tasklist.title)
        self.assertContains(response, self.task.title)
        self.assertNotContains(response, SHOULD_NOT_CONTAIN_TEXT)
        self.client.logout()

    def test_tasklist_create_view(self):
        path = reverse('tasklist-create')
        # without authentication
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(no_response, get_redirected_login_url(path))
        # with authentication
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, 'Create')
        self.assertNotContains(get_response, 'Update')
        self.assertTemplateUsed(get_response, 'tasklists/tasklist_create.html')
        # post
        data = {
            'title': 'new tasklist'
        }
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        new_tasklist = TaskList.objects.first()
        self.assertEqual(new_tasklist.title, data['title'])
        # adds user automatically
        self.assertEqual(new_tasklist.user, self.user)
        self.assertRedirects(post_response, new_tasklist.get_absolute_url())
        self.client.logout()

    def test_tasklist_update_view(self):
        path = reverse('tasklist-update', kwargs={'slug': self.tasklist.slug})
        # absolute update url test
        self.assertEqual(self.tasklist.get_absolute_update_url(), path)
        # without authentication
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(no_response, get_redirected_login_url(path))
        # with authentication but not user itself
        self.client.force_login(self.bad_user)
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
        # with authentication and user itself
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, 'Update')
        self.assertContains(get_response, self.tasklist.title)
        self.assertNotContains(get_response, 'Create')
        self.assertTemplateUsed(get_response, 'tasklists/tasklist_update.html')
        # post
        data = {
            'title': 'updated',
        }
        post_response = self.client.post(path, data)
        requested_time = timezone.now()
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.tasklist.refresh_from_db()
        self.assertRedirects(post_response, self.tasklist.get_absolute_url())
        self.assertEqual(self.tasklist.title, 'updated')
        self.assertAlmostEqual(self.tasklist.updated_at, requested_time, delta=timezone.timedelta(minutes=1))
        self.client.logout()

    def test_tasklist_delete_view(self):
        path = reverse('tasklist-delete', kwargs={'slug': self.tasklist.slug})
        # absolute delete url test
        self.assertEqual(self.tasklist.get_absolute_delete_url(), path)
        # without authentication
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(no_response, get_redirected_login_url(path))
        # with authentication but not user itself
        self.client.force_login(self.bad_user)
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
        # with authentication and user itself
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, 'Delete')
        self.assertContains(get_response, self.tasklist.title)
        self.assertNotContains(get_response, 'Create')
        self.assertTemplateUsed(get_response, 'tasklists/tasklist_delete.html')
        # delete
        delete_response = self.client.delete(path)
        self.assertEqual(delete_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(delete_response, reverse('tasklist-list'))
        self.assertFalse(TaskList.objects.filter(id=self.tasklist.id).exists())
        self.client.logout()
