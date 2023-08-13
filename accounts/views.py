from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


class UserProfile(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/user_detail.html'

    def get_object(self, queryset=None):
        if not self.kwargs.get('slug'):
            return self.request.user
        return super().get_object(queryset)

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user


