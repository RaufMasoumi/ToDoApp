from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from .models import Task, TaskList
# Create your views here.


class AllauthLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('account_login')


class TaskListUserQuerysetMixin:
    request = None

    def get_queryset(self):
        return TaskList.objects.user_tasklist(user=self.request.user)


class TaskListListView(AllauthLoginRequiredMixin, TaskListUserQuerysetMixin, ListView):
    context_object_name = 'tasklists'
    template_name = 'tasks/tasklist_list.html'


class TaskListDetailView(AllauthLoginRequiredMixin, TaskListUserQuerysetMixin, DetailView):
    context_object_name = 'tasklist'
    template_name = 'tasks/tasklist_detail.html'


class TaskListCreateView(AllauthLoginRequiredMixin, CreateView):
    model = TaskList
    template_name = 'tasks/tasklist_create.html'
    fields = ('title', 'tasks')

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskListDeleteView(AllauthLoginRequiredMixin, TaskListUserQuerysetMixin, DeleteView):
    context_object_name = 'tasklist'
    template_name = 'tasks/tasklist_delete.html'

    def get_success_url(self):
        return reverse('tasklist-list')

