from django.shortcuts import reverse
from django.test import TestCase
from rest_framework import status
from .mixins import TestUserSetUpMixin, ViewBadUserTestsMixin, ViewSOFMixin, ViewSOFSupportingTestsMixin
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


class TaskValidationTests(TestUserSetUpMixin, TestCase):

    def setUp(self):
        self.task = Task.objects.create(
            user=self.user,
            title='testtask'
        )

    def test_task_status_validation(self, update_path=None, update_method='post'):
        self.client.force_login(self.user)
        update_path = update_path if update_path else self.task.get_absolute_update_url()
        data = {'title': self.task.title, 'is_important': True, 'is_not_important': True}
        getattr(self.client, update_method)(update_path, data)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_important)
        self.assertFalse(self.task.is_not_important)
        self.client.logout()


class ViewSOFMixinTests(TestUserSetUpMixin, TestCase):
    need_bad_user = False
    using_mixin_view_path = reverse('task-list')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.tasks = []
        for i in range(4):
            task = Task.objects.create(
                user=cls.user,
                title=f'task{i+1}'
            )
            cls.tasks.append(task)

    def test_mixin_searching(self):
        self.client.force_login(self.user)
        # all task scenario
        data1 = {
            'search': 'task'
        }
        response1 = self.client.get(self.using_mixin_view_path, data1)
        for task in self.tasks:
            self.assertIn(task, response1.context['filter'].qs)
            self.assertContains(response1, task.title)
        # one tasks scenario
        data2 = {
            'search': 'task1'
        }
        response2 = self.client.get(self.using_mixin_view_path, data2)
        self.assertContains(response2, self.tasks[0])
        for task in self.tasks[1:]:
            self.assertNotIn(task, response2.context['filter'].qs)
            self.assertNotContains(response2, task.title)
        # no tasks scenario
        data3 = {
            'search': 'hello search!'
        }
        response3 = self.client.get(self.using_mixin_view_path, data3)
        for task in self.tasks:
            self.assertNotIn(task, response3.context['filter'].qs)
            self.assertNotContains(response3, task.title)
        self.client.logout()

    def test_mixin_ordering(self):
        self.client.force_login(self.user)
        # ascending title ordering scenario
        data1 = {
            'ordering': 'title'
        }
        response1 = self.client.get(self.using_mixin_view_path, data1)
        should_be_queryset = sorted(self.tasks, key=lambda task: task.title)
        self.assertQuerysetEqual(response1.context['filter'].qs, should_be_queryset, ordered=True)
        # descending title ordering scenario
        data2 = {
            'ordering': '-title'
        }
        response2 = self.client.get(self.using_mixin_view_path, data2)
        should_be_queryset = sorted(self.tasks, key=lambda task: task.title, reverse=True)
        self.assertQuerysetEqual(response2.context['filter'].qs, should_be_queryset, ordered=True)
        self.client.logout()

    def test_mixin_filtering(self):
        self.client.force_login(self.user)
        # all tasks filtering scenario
        data1 = {
            'title__icontains': 'task'
        }
        response1 = self.client.get(self.using_mixin_view_path, data1)
        self.assertQuerysetEqual(response1.context['filter'].qs, self.tasks, ordered=False)
        for task in self.tasks:
            self.assertContains(response1, task)
        # one task scenario
        data2 = {
            'title__iexact': 'task1'
        }
        response2 = self.client.get(self.using_mixin_view_path, data2)
        self.assertQuerysetEqual(response2.context['filter'].qs, self.tasks[0:1])
        self.assertContains(response2, self.tasks[0])
        for task in self.tasks[1:]:
            self.assertNotContains(response2, task)
        # no tasks scenario
        data3 = {
            'is_done': True
        }
        response3 = self.client.get(self.using_mixin_view_path, data3)
        self.assertQuerysetEqual(response3.context['filter'].qs, [])
        for task in self.tasks:
            self.assertNotContains(response3, task)
        self.client.logout()


class TaskSOFTests(TestUserSetUpMixin, ViewSOFSupportingTestsMixin, TestCase):
    need_bad_user = False

    def test_task_list_view_supports_sof(self):
        self.view_sof_test(reverse('task-list'))
