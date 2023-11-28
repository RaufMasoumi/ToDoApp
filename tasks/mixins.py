from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from rest_framework import status


class AllauthLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('account_login')


class UserTaskQuerysetMixin:
    request = None

    def get_queryset(self):
        return self.request.user.tasks.all()


class TestUserSetUpMixin:
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

    def get_bad_user(self):
        return getattr(self, 'bad_user', None)


class ViewBadUserTestsMixin(TestUserSetUpMixin):

    def login_required_test(self, path):
        # without authentication
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(no_response, get_redirected_login_url(path))

    def user_itself_or_somecode_test(self, path, method='get', bad_user=None, status_code=status.HTTP_404_NOT_FOUND):
        bad_user = bad_user or self.get_bad_user()
        method = method if method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'trace'] else 'get'
        # with authentication but not user itself
        self.client.force_login(bad_user)
        no_response = getattr(self.client, method)(path)
        self.assertEqual(no_response.status_code, status_code)
        self.client.logout()

    def user_itself_or_200_but_nothing_exists_test(self, path, bad_user=None, should_not_contain_content=tuple()):
        bad_user = bad_user or self.get_bad_user()
        # with authentication but not user itself
        self.client.force_login(bad_user)
        no_response = self.client.get(path)
        self.assertEqual(no_response.status_code, status.HTTP_200_OK)
        for content in should_not_contain_content:
            self.assertNotContains(no_response, content)
        self.client.logout()

    def login_required_and_user_itself_or_somecode_test(
            self, path, method='get', bad_user=None, status_code=status.HTTP_404_NOT_FOUND
    ):
        self.login_required_test(path)
        self.user_itself_or_somecode_test(path, method, bad_user, status_code)

    def login_required_and_user_itself_or_nothing_exists_test(
            self, path, bad_user=None, should_not_contain_content=None
    ):
        self.login_required_test(path)
        self.user_itself_or_200_but_nothing_exists_test(path, bad_user, should_not_contain_content)


# SOF stands for Searching, Ordering, Filtering
class ViewSOFMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        queryset = self.get_queryset()
        self.request.query_params = self.request.GET
        queryset = self.ordering_filter_class().filter_queryset(self.request, queryset, self)
        queryset = self.search_filter_class().filter_queryset(self.request, queryset, self)
        context['filter'] = self.filterset_class(self.request.GET, queryset)
        context['search_form'] = self.search_form(self.request.GET)
        context['ordering_form'] = self.ordering_form(self.request.GET)
        return context


def get_redirected_login_url(coming_from):
    return reverse('account_login') + f'?next={coming_from}'
