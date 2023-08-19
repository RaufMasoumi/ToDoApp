from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
# Create your views here.


class AllauthLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('account_login')


class UserTaskQuerysetMixin:
    request = None

    def get_queryset(self):
        return Task.objects.user_task(self.request.user)


class TaskDetailView(AllauthLoginRequiredMixin, UserTaskQuerysetMixin, DetailView):
    template_name = 'tasks/task_detail.html'


class TaskCreateView(AllauthLoginRequiredMixin, CreateView):
    model = Task
    fields = ('title', 'due_date', 'is_important', 'is_not_important', 'is_timely_important')
    template_name = 'tasks/task_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AllauthLoginRequiredMixin, UserTaskQuerysetMixin, UpdateView):
    fields = ('title', 'due_date', 'is_important', 'is_not_important', 'is_timely_important')
    template_name = 'tasks/task_update.html'


class TaskDeleteView(AllauthLoginRequiredMixin, UserTaskQuerysetMixin, DeleteView):
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        success_url = self.success_url
        get = self.request.GET
        if get.get('tasklist'):
            tasklist = self.request.user.tasklists.get(slug=get['tasklist'])
            success_url = tasklist.get_absolute_url()
        return success_url
