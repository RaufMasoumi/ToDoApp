from django.test import TestCase, SimpleTestCase
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import status
from tasks.models import Task, DEFAULT_TASKLISTS, DEFAULT_TASK_STATUSES
from tasks.tests import CustomTestCase, SHOULD_NOT_CONTAIN_TEXT
from tasks.mixins import TestUserSetUpMixin, ViewSOFSupportingTestsMixin
from .models import TaskList
from .filters import TaskListFilterSet, TASKLIST_FILTERSETS_LIST

# Create your tests here.


class DefaultTaskListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.default_tasklist_permission = Permission.objects.get(codename='default_tasklist')

    def test_user_default_tasklists_auto_creation(self):
        self.assertQuerysetEqual(self.user.tasklists.default_tasklists(), self.user.tasklists.filter(is_default=True))
        self.assertEqual(self.user.tasklists.default_tasklists().count(), len(DEFAULT_TASKLISTS))
        for getter, title in DEFAULT_TASKLISTS.items():
            self.assertEqual(getattr(self.user.tasklists, getter)(), self.user.tasklists.get(title=title))

    def test_user_default_tasklists_permission(self):
        # without permission
        self.client.force_login(self.user)
        path = reverse('tasklist-update', kwargs={'slug': 'all-tasks'})
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_403_FORBIDDEN)
        # with permission
        self.user.user_permissions.add(self.default_tasklist_permission)
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()


class TaskListTests(CustomTestCase):

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
        self.assertEqual(TaskList.objects.filter(is_default=False).count(), 2)
        tasklist = TaskList.objects.get(pk=self.tasklist.pk)
        self.assertEqual(tasklist, self.tasklist)
        self.assertEqual(tasklist.title, 'testtasklist')

    def test_tasklist_slug_auto_creation(self):
        self.assertEqual(self.tasklist.slug, 'testtasklist')

    def test_tasklist_list_view(self):
        path = reverse('tasklist-list')
        # bad user test
        content = [self.tasklist.title, self.tasklist2.title]
        self.login_required_and_user_itself_or_nothing_exists_test(path, should_not_contain_content=content)
        # correct user test
        self.client.force_login(self.user)
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # created tasklists + user default tasklists
        self.assertEqual(len(response.context.get('tasklists')), 6)
        for content in content:
            self.assertContains(response, content)
        self.assertNotContains(response, SHOULD_NOT_CONTAIN_TEXT)
        self.assertTemplateUsed(response, 'tasklists/tasklist_list.html')

    def test_tasklist_detail_view(self):
        path = reverse('tasklist-detail', kwargs={'slug': self.tasklist.slug})
        # absolute url test
        self.assertEqual(self.tasklist.get_absolute_url(), path)
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
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
        # bad user test
        self.login_required_test(path)
        # correct user test
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
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
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
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, 'Delete')
        self.assertContains(get_response, self.tasklist.title)
        self.assertNotContains(get_response, 'Create')
        self.assertTemplateUsed(get_response, 'tasklists/tasklist_delete.html')
        # post(as delete)
        delete_response = self.client.post(path)
        self.assertEqual(delete_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(delete_response, reverse('tasklist-list'))
        self.assertFalse(TaskList.objects.filter(id=self.tasklist.id).exists())
        self.client.logout()


class DefaultTaskListTaskTests(TestUserSetUpMixin, TestCase):
    need_bad_user = False

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.default_tasklist_permission = Permission.objects.get(codename='default_tasklist')

    def setUp(self):
        self.task = Task.objects.create(
            user=self.user,
            title='testtask'
        )

    def test_add_and_remove_task_of_default_tasklist_signal(self):
        for getter, is_status in DEFAULT_TASK_STATUSES.items():
            default_tasklist_title = DEFAULT_TASKLISTS[getter]
            setattr(self.task, is_status, False)
            self.task.save()
            setattr(self.task, is_status, True)
            self.task.save()
            self.assertTrue(self.task.tasklists.filter(title=default_tasklist_title).exists())
            setattr(self.task, is_status, False)
            self.task.save()
            self.assertFalse(self.task.tasklists.filter(title=default_tasklist_title).exists())

    def test_add_and_remove_task_of_all_tasks(self):
        self.assertTrue(self.task.tasklists.filter(title=DEFAULT_TASKLISTS['all_tasks']).exists())
        self.task.delete()
        self.assertEqual(self.user.tasklists.all_tasks().tasks.count(), 0)

    def test_default_tasklist_task_permission(self):
        self.client.force_login(self.user)
        path = reverse('tasklist-task-create', kwargs={'tasklist': 'all-tasks'})
        # without permission
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_403_FORBIDDEN)
        # with permission
        self.user.user_permissions.add(self.default_tasklist_permission)
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()


class TaskListValidationTests(TestUserSetUpMixin, TestCase):
    def setUp(self):
        self.tasklist = TaskList.objects.create(
            user=self.user,
            title='testtasklist',
        )
        self.task = Task.objects.create(
            user=self.user,
            title='testtask'
        )
        self.bad_user_task = Task.objects.create(
            user=self.bad_user,
            title='testtask2'
        )

    def test_tasklist_title_validation(self, create_path=None, update_path=None, update_method='post'):
        self.client.force_login(self.user)
        create_path = create_path if create_path else reverse('tasklist-create')
        data = {'title': 'testtasklist'}
        should_be_title = f'{self.tasklist.title}(1)'
        self.client.post(create_path, data)
        tasklist = TaskList.objects.order_by('-created_at').first()
        self.assertNotEqual(tasklist.title, data['title'])
        self.assertEqual(tasklist.title, should_be_title)
        update_path = update_path if update_path else reverse('tasklist-update', kwargs={'slug': tasklist.slug})
        getattr(self.client, update_method)(update_path, data)
        tasklist.refresh_from_db()
        self.assertEqual(tasklist.title, should_be_title)
        self.client.logout()

    def test_tasklist_tasks_validation(self):
        self.client.force_login(self.user)
        path = reverse('tasklist-update', kwargs={'slug': self.tasklist.slug})
        data = {
            'title': self.tasklist.title,
            'tasks': [self.task.pk, self.bad_user_task.pk]
        }
        self.client.post(path, data)
        self.assertEqual(self.tasklist.tasks.count(), 1)
        self.assertTrue(self.tasklist.tasks.filter(pk=self.task.pk).exists())
        self.assertFalse(self.tasklist.tasks.filter(pk=self.bad_user_task.pk).exists())
        self.client.logout()


class TaskListSOFTests(TestUserSetUpMixin, ViewSOFSupportingTestsMixin, TestCase):
    need_bad_user = False

    def test_tasklist_list_view_supports_sof(self):
        self.view_sof_test(reverse('tasklist-list'))


class TaskListTaskTests(CustomTestCase):

    def setUp(self):
        self.tasklist = TaskList.objects.create(
            user=self.user,
            title='testtasklist',
        )
        self.task = Task.objects.create(
            user=self.user,
            title='testtask'
        )
        self.tasklist.tasks.add(self.task)

    def test_tasklist_task_create_view(self):
        path = reverse('tasklist-task-create', kwargs={'tasklist': self.tasklist.slug})
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, 'Create')
        self.assertContains(get_response, self.tasklist.title)
        self.assertNotContains(get_response, 'Update')
        self.assertTemplateUsed(get_response, 'tasklists/tasklist_task_create.html')
        # post
        data = {
            'title': 'new task',
            'user': self.bad_user
        }
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        created_task = Task.objects.first()
        self.assertEqual(created_task.title, data['title'])
        # user set to the requested user anytime
        self.assertEqual(created_task.user, self.user)
        # task added to the tasklist
        self.assertTrue(self.tasklist.tasks.filter(pk=created_task.pk).exists())
        self.client.logout()

    def test_tasklist_task_update_view(self):
        path = reverse('tasklist-task-update', kwargs={
            'tasklist': self.tasklist.slug,
            'pk': self.task.pk
        })
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, 'Update')
        self.assertContains(get_response, self.task.title)
        self.assertNotContains(get_response, SHOULD_NOT_CONTAIN_TEXT)
        self.assertTemplateUsed(get_response, 'tasks/task_update.html')
        # post
        data = {
            'title': 'updated'
        }
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(post_response, self.tasklist.get_absolute_url())
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, data['title'])
        self.client.logout()

    def test_tasklist_task_delete_view(self):
        path = reverse('tasklist-task-delete', kwargs={
            'tasklist': self.tasklist.slug,
            'pk': self.task.pk
        })
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, 'Remove')
        self.assertContains(get_response, self.task.title)
        self.assertContains(get_response, self.tasklist.title)
        self.assertNotContains(get_response, 'Update')
        self.assertTemplateUsed(get_response, 'tasklists/tasklist_task_delete.html')
        # post (as delete)
        post_response = self.client.post(path)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(post_response, self.tasklist.get_absolute_url())
        self.assertFalse(self.tasklist.tasks.filter(pk=self.task.pk).exists())
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        self.client.logout()


class DjangoFiltersMiddlewareTests(TestUserSetUpMixin, TestCase):
    sof_supporting_view_path = reverse('tasklist-list')

    def test_middleware_does_not_affect_empty_request(self):
        self.client.force_login(self.user)
        response = self.client.get(self.sof_supporting_view_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_middleware_does_not_affect_non_related_request(self):
        self.client.force_login(self.user)
        data = {
            'hello': 'world!'
        }
        response = self.client.get(self.sof_supporting_view_path, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_middleware_does_not_affect_proper_request(self):
        self.client.force_login(self.user)
        data = {
            'title__iexact': 'testtasklist'
        }
        response = self.client.get(self.sof_supporting_view_path, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_middleware_changes_improper_request(self):
        self.client.force_login(self.user)
        data = {
            'title__iexact': 'testtasklist',
            'title__icontains': ''
        }
        response = self.client.get(self.sof_supporting_view_path, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        new_data = {k: v for k, v in data.items() if v}
        kwargs = '+'.join([f'{k}={v}' for k, v in new_data.items()])
        self.assertRedirects(response, f'{self.sof_supporting_view_path}?{kwargs}')
        self.client.logout()

    def test_middleware_removes_question_mark_on_empty_url(self):
        self.client.force_login(self.user)
        data = {
            'title__iexact': ''
        }
        response = self.client.get(self.sof_supporting_view_path, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, self.sof_supporting_view_path)
        self.assertEqual(response.url.find('?'), -1)
        self.client.logout()


class TaskListFilterSetsTests(SimpleTestCase):
    def test_django_filters_middleware_supports_tasklist_filterset(self):
        self.assertIn(TaskListFilterSet, TASKLIST_FILTERSETS_LIST)
