from django.shortcuts import reverse
from rest_framework import status
from tasks.api_tests import CustomAPITestCase, SHOULD_NOT_CONTAIN_TEXT
from tasks.models import Task
from .models import Category


class CategoryAPITests(CustomAPITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(
            user=self.user,
            title='testcategory1',
        )
        self.category2 = Category.objects.create(
            user=self.user,
            title='testcategory2',
        )

    def test_category_lc_api_view(self):
        path = reverse('api-category-list')
        content = [self.category1.title, self.category2.title]
        # bad user tests
        self.login_required_and_user_itself_or_nothing_exists_test(path, should_not_contain_content=content)
        # correct user tests
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        for single_content in content:
            self.assertContains(get_response, single_content)
        self.assertNotContains(get_response, SHOULD_NOT_CONTAIN_TEXT)
        # post
        data = {
            'title': 'newcategory'
        }
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Category.objects.order_by('-created_at').first().title, data['title'])
        self.client.logout()

    def test_category_rud_api_view(self):
        path = reverse('api-category-detail', kwargs={'slug': self.category1.slug})
        # absolute api url test
        self.assertEqual(self.category1.get_absolute_api_url(), path)
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.category1.title)
        self.assertNotContains(get_response, self.category2.title)
        # put
        data = {
            'title': 'updated'
        }
        put_response = self.client.put(path, data)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.title, data['title'])
        # delete
        # title and slug have been changed, so using absolute url
        delete_response = self.client.delete(self.category1.get_absolute_api_url())
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)
        self.assertFalse(Category.objects.filter(pk=self.category1.pk).exists())
        self.client.logout()


class CategoryTaskAPITests(CustomAPITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            user=self.user,
            title='testcategory'
        )
        self.task = Task.objects.create(
            user=self.user,
            title='testtask'
        )
        self.task.categories.add(self.category)

    def test_category_task_lc_api_view(self):
        path = reverse('api-category-task-list', kwargs={'category': self.category.slug})
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.client.get(path)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertContains(get_response, self.task.title)
        self.assertNotContains(get_response, SHOULD_NOT_CONTAIN_TEXT)
        # post
        data = {
            'title': 'newtask'
        }
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.category.tasks.count(), 2)
        self.assertEqual(self.category.tasks.order_by('-created_at').first().title, data['title'])
        self.client.logout()

    def test_category_task_destroy_api_view(self):
        path = reverse('api-category-task-delete', kwargs={'category': self.category.slug, 'pk': self.task.pk})
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path, method='delete')
        # correct user test
        self.client.force_login(self.user)
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.category.tasks.count(), 0)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        self.client.logout()
