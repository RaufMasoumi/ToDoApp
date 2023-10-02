from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class AllauthLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('account_login')


class UserTaskQuerysetMixin:
    request = None

    def get_queryset(self):
        return self.request.user.tasks.all()
