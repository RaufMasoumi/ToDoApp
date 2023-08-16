from django.shortcuts import render
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .models import Task
# Create your views here.


class AllauthLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('account_login')


class TaskUpdateView(UpdateView):
    fields = ('title', 'due_date', 'is_important', 'is_not_important', 'is_timely_important')
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Task.objects.user_task(self.request.user)

