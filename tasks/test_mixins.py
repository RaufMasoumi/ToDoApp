from django.test import TestCase
from django.shortcuts import reverse, resolve_url
from django.urls import NoReverseMatch
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ValidationError
from rest_framework import status
from .tests import SHOULD_NOT_CONTAIN_TEXT
from .mixins import ViewBadUserTestsMixin


def test_decorator_maker(func):
    def args_getter(*args, **kwargs):
        def test_function_getter(test_func):
            def wrapper(self):
                path_args = ['path', 'success_url']
                content_args = ['content', 'not_contain_content', 'bad_user_not_contain_content']
                data_args = ['data', ]
                object_name = kwargs.get('object_name', None)
                if object_name:
                    obj = getattr(self, object_name, None)
                    if obj:
                        kwargs['obj'] = obj
                for k, v in kwargs.items():
                    if k in path_args:
                        url_kwargs = kwargs.get('url_kwargs', None)
                        lookup_fields = kwargs.get('lookup_fields', None)
                        kwargs[k] = get_path(path=v, url_kwargs=url_kwargs, lookup_fields=lookup_fields, obj=kwargs.get('obj', None),
                                             dont_raise=True)
                    if k in content_args:
                        kwargs[k] = get_content(content=v, obj=self, name=k)
                    if k in data_args:
                        kwargs[k] = get_data(data=v, obj=self, name=k)
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

    def create_test(self, path, model, data, success_url=None, lookup_fields=None):
        created_obj = None

        @receiver(post_save, sender=model)
        def get_created_obj(sender, instance, created, **kwargs):
            if created:
                nonlocal created_obj
                created_obj = instance

        before_create_count = model.objects.count()
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(model.objects.count(), before_create_count + 1)
        for field, value in data.items():
            self.assertEqual(getattr(created_obj, field), value)
        success_url = get_path(path=success_url, lookup_fields=lookup_fields, obj=created_obj)
        self.assertRedirects(post_response, success_url)
        return post_response, created_obj, success_url

    def update_test(self, path, obj, data, success_url=None):
        post_response = self.client.post(path, data)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        obj.refresh_from_db()
        success_url = obj.get_absolute_url() if not success_url else success_url
        self.assertRedirects(post_response, success_url)
        for field, updated_value in data.items():
            self.assertEqual(getattr(obj, field), updated_value)
        return post_response, obj, success_url

    def delete_test(self, path, obj, success_url, method='post'):
        method = method if method in ['post', 'delete'] else 'post'
        post_response = getattr(self.client, method)(path)
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(post_response, success_url)
        self.assertFalse(obj.__class__.objects.filter(pk=obj.pk).exists())
        return post_response, obj


class GenericViewsTestCase(ViewBadUserTestsMixin, CRUDFunctionalityTestCase):

    # The decorated function must receive three positional arguments in order of: path, response, content
    @test_decorator_maker
    def list_view_test(
        self, view_test_func, path: str, content: list, context_name: str, object_list_count: int,
        template_name: str, not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, ), bad_user_not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, ),
        **kwargs
    ):
        # bad user test
        self.login_required_and_user_itself_or_nothing_exists_test(path, should_not_contain_content=bad_user_not_contain_content)
        # correct user test
        self.client.force_login(self.user)
        response = self.list_test(path, content, context_name, object_list_count, template_name, not_contain_content)
        # run additional tests by test func itself
        view_test_func(self, path, response, content)
        self.client.logout()

    # The decorated function must receive three positional arguments in order of: path, response, content, obj
    @test_decorator_maker
    def detail_view_test(
        self, view_test_func, path: str, content: list, template_name: str, obj,  not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, ),
        bad_user_status_code=status.HTTP_404_NOT_FOUND, **kwargs
    ):
        # absolute url test
        self.assertEqual(obj.get_absolute_url(), path)
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path, status_code=bad_user_status_code)
        # correct user test
        self.client.force_login(self.user)
        response = self.detail_test(path, content, template_name, not_contain_content)
        # run additional tests by test func itself
        view_test_func(self, path, response, content, obj)
        self.client.logout()

    @test_decorator_maker
    def create_view_test(
        self, view_test_func, path: str, content: list, template_name: str, model, data: dict, lookup_fields=None,
        not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, ), success_url=None, **kwargs
    ):
        # bad user test
        self.login_required_test(path)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.detail_test(path, content, template_name, not_contain_content)
        # post
        post_response, created_object, success_url = self.create_test(path, model, data, success_url, lookup_fields)
        # adds user automatically
        self.assertEqual(created_object.user, self.user)
        # run additional tests by test func itself
        view_test_func(self, path, data, get_response, post_response, created_object, success_url)
        self.client.logout()

    @test_decorator_maker
    def update_view_test(
        self, view_test_func, path: str, content: list, template_name: str, data: dict, obj, not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, ),
        bad_user_status_code=status.HTTP_404_NOT_FOUND, success_url=None,  **kwargs,
    ):
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path, status_code=bad_user_status_code)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.detail_test(path, content, template_name, not_contain_content)
        # post
        post_response, updated_object, success_url = self.update_test(path, obj, data, success_url)
        # run additional tests by test func itself
        view_test_func(self, path, data, get_response, post_response, updated_object, success_url)
        self.client.logout()

    @test_decorator_maker
    def delete_view_test(
        self, view_test_func, path: str, content: list, template_name: str, obj,  success_url: str,
        not_contain_content=(SHOULD_NOT_CONTAIN_TEXT, ), bad_user_status_code=status.HTTP_404_NOT_FOUND, method='post', **kwargs
    ):
        # bad user test
        self.login_required_and_user_itself_or_somecode_test(path, status_code=bad_user_status_code)
        # correct user test
        self.client.force_login(self.user)
        # get
        get_response = self.detail_test(path, content, template_name, not_contain_content)
        # post
        post_response, deleted_obj = self.delete_test(path, obj, success_url, method=method)
        # run additional tests by test func itself
        view_test_func(self, path, get_response, post_response, deleted_obj, success_url)
        self.client.logout()


def get_content(content=None, obj=None, name='content'):
    if content is None:
        content = []
    if is_iterable(content):
        return content
    elif isinstance(content, str) and obj:
        content = getattr(obj, content, None)
        return get_content(content, obj, name)
    else:
        raise ValidationError(
                f'The {name} should be iterable (as list, tuple or set), but it is {type(content)} type.'
            )


def get_data(data=None, obj=None, name='data'):
    if data is None:
        data = {}
    if is_dict(data):
        return data
    elif isinstance(data, str):
        data = getattr(obj, data, None)
        return get_data(data, obj, name)
    else:
        raise ValidationError(f'The passed data should be a dict or TestCase instance attribute name but it is {type(data)} type.')


def get_path(path=str(), url_kwargs=None, lookup_fields=None, obj=None, dont_raise=False):
    if path is None:
        path = str()
    if url_kwargs is None:
        url_kwargs = dict()
    if lookup_fields is None:
        lookup_fields = dict()
    if not is_iterable(lookup_fields) and not isinstance(lookup_fields, dict):
        raise ValidationError(
            f'The lookup_fields is not a valid type. It should be either an iterable of lookup fields (as list, tuple or set), or lookup_field: TestCase instance_field_name mapping (as dict), but it is {type(lookup_fields)} type.'
        )
    if not isinstance(url_kwargs, dict):
        raise ValidationError(f'The url_kwargs should be a dict, but it is {type(url_kwargs)} type')
    if lookup_fields and not obj:
        raise ValidationError('If lookup_fields is passed, so the obj must be passed')
    lookup_fields_kwargs = make_url_kwargs_with_lookup_fields(lookup_fields, obj)
    kwargs = url_kwargs.copy()
    kwargs.update(lookup_fields_kwargs)
    try:
        path = resolve_url(path, **kwargs)
    except NoReverseMatch:
        if obj:
            path = resolve_url(obj)
        else:
            if dont_raise:
                return None
            else:
                raise
    return path


# lookup_fields can be each list based or dict based in order of:
# list if the lookup field is same with the object field name -> [field1, field2, ...]
# dict if the lookup filed is not same with the object field name -> {lookup_field:obj_field_name, ...}
def make_url_kwargs_with_lookup_fields(lookup_fields, obj):
    kwargs = dict()
    if is_iterable(lookup_fields):
        kwargs = {k: getattr(obj, k, None) for k in lookup_fields}
    elif isinstance(lookup_fields, dict):
        kwargs = {k: getattr(obj, v, None) for k, v in lookup_fields.items()}
    return kwargs


def is_iterable(var):
    return isinstance(var, (list, tuple, set))


def is_dict(var):
    return isinstance(var, dict)

