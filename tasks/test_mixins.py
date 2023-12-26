from django.test import TestCase
from rest_framework import status
from .tests import SHOULD_NOT_CONTAIN_TEXT
from .mixins import ViewBadUserTestsMixin


def test_decorator_maker(func):
    def args_getter(*args, **kwargs):
        def test_function_getter(test_func):
            def wrapper(self):
                func(self, test_func, *args, **kwargs)
            return wrapper
        return test_function_getter
    return args_getter


class CRUDFunctionalityTestCase(TestCase):
    def list_test(
            self, path: str, content: list, context_name: str, object_list_count: int,
            template_name: str, not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, )
    ):
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context.get(context_name)), object_list_count)
        for single_content in content:
            self.assertContains(response, single_content)
        for single_content in not_contain_content:
            self.assertNotContains(response, single_content)
        self.assertTemplateUsed(response, template_name)
        return response

    def detail_test(
            self, path: str, content: list, template_name: str, not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, )
    ):
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for single_content in content:
            self.assertContains(response, single_content)
        for single_content in not_contain_content:
            self.assertNotContains(response, single_content)
        self.assertTemplateUsed(response, template_name)
        return response

    def create_test(self, path, model, data, success_url, lookup_method='first'):
        before_create_count = model.objects.count()
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(model.objects.count(), before_create_count + 1)
        created_obj = getattr(model.objects, lookup_method)()
        for field, value in data.items():
            self.assertEqual(getattr(created_obj, field), value)
        self.assertRedirects(post_response, success_url)
        return post_response, created_obj

    def update_test(self, path, obj, data, success_url):
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(post_response, success_url)
        obj.refresh_from_db()
        for field, updated_value in data.items():
            self.assertEqual(getattr(obj, field), updated_value)
        return post_response, obj

    def delete_test(self, path, obj, success_url):
        post_response = self.client.post(path)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(post_response, success_url)
        self.assertFalse(obj.__class__.objects.filter(pk=obj.pk).exists())
        return post_response, obj


class GenericViewsTestCase(ViewBadUserTestsMixin, CRUDFunctionalityTestCase):

    @test_decorator_maker
    def list_view_test(
                self, view_test_func, path: str, content: list, context_name: str, object_list_count: int,
                template_name: str, not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, ),
                bad_user_not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, )
    ):
        content = get_content(self, content)
        not_contain_content = get_content(self, not_contain_content)
        bad_user_not_contain_content = get_content(self, bad_user_not_contain_content)
        # bad user test
        self.login_required_and_user_itself_or_nothing_exists_test(
            path, should_not_contain_content=bad_user_not_contain_content
        )
        # correct user test
        self.client.force_login(self.user)
        response = self.list_test(path, content, context_name, object_list_count, template_name, not_contain_content)
        # run additional tests by test func itself
        view_test_func(self, path, response, content)
        self.client.logout()

    @test_decorator_maker
    def detail_view_test(
            self, view_test_func, path: str, content: list, template_name: str, object_name: str,
            not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, ), bad_user_status_code=status.HTTP_404_NOT_FOUND
    ):
        obj = getattr(self, object_name, None)
        content = get_content(self, content)
        not_contain_content = get_content(self, not_contain_content)
        # absolute url test
        self.assertEqual(obj.get_absolute_url(), path)
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path, status_code=bad_user_status_code)
        # correct user test
        self.client.force_login(self.user)
        response = self.detail_test(path, content, template_name, not_contain_content)
        # run additional tests by test func itself
        view_test_func(self, path, response, content)
        self.client.logout()

    @test_decorator_maker
    def create_view_test(
            self, view_test_func, path: str, content: list, template_name: str, model, data: dict,
            not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, ), success_url=None, lookup_method='first'
    ):
        content = get_content(self, content)
        not_contain_content = get_content(self, not_contain_content)
        # bad user test
        self.login_required_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.detail_test(path, content, template_name, not_contain_content)
        # post
        post_response, created_object = self.create_test(path, model, data, success_url, lookup_method)
        # adds user automatically
        self.assertEqual(created_object.user, self.user)
        # run additional tests by test func itself
        view_test_func(self, path, data, get_response, post_response, created_object)
        self.client.logout()

    @test_decorator_maker
    def update_view_test(
            self, view_test_func, path: str, content: list, template_name: str, object_name: str, data: dict,
            not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, ), bad_user_status_code=status.HTTP_404_NOT_FOUND,
            success_url=None
    ):
        obj = getattr(self, object_name, None)
        content = get_content(self, content)
        not_contain_content = get_content(self, not_contain_content)
        success_url = obj.get_absolute_url() if not success_url else success_url
        # absolute update url test
        self.assertEqual(obj.get_absolute_update_url(), path)
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path, status_code=bad_user_status_code)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.detail_test(path, content, template_name, not_contain_content)
        # post
        post_response, updated_object = self.update_test(path, obj, data, success_url)
        # run additional tests by test func itself
        view_test_func(self, path, data, get_response, post_response, updated_object)
        self.client.logout()

    @test_decorator_maker
    def delete_view_test(
            self, view_test_func, path: str, content: list, template_name: str, object_name: str, success_url: str,
            not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, ), bad_user_status_code=status.HTTP_404_NOT_FOUND
    ):
        obj = getattr(self, object_name, None)
        content = get_content(self, content)
        not_contain_content = get_content(self, not_contain_content)
        # absolute delete url test
        self.assertEqual(obj.get_absolute_delete_url(), path)
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path, status_code=bad_user_status_code)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.detail_test(path, content, template_name, not_contain_content)
        # post
        post_response, deleted_obj = self.delete_test(path, obj, success_url)
        # run additional tests by test func itself
        view_test_func(path, get_response, post_response, deleted_obj)
        self.client.logout()


def get_content(obj, content):
    if isinstance(content, (list, tuple, set)):
        return content
    elif isinstance(content, str):
        return getattr(obj, content, None)
