from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Task, TaskList

# Create your views here.


class AllauthLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('accounts_login')


class TaskListListView(AllauthLoginRequiredMixin, ListView):
    context_object_name = 'tasklists'
    template_name = 'tasks/tasklist_list.html'

    def get_queryset(self):
        return TaskList.objects.filter(user=self.request.user)


class TaskListDetailView(AllauthLoginRequiredMixin, DetailView):
    context_object_name = 'tasklist'
    template_name = 'tasks/tasklist_detail.html'

    def get_queryset(self):
        return TaskList.objects.filter(user=self.request.user)


class TaskListCreateView(AllauthLoginRequiredMixin, CreateView):
    model = TaskList
    template_name = 'tasks/tasklist_create.html'
    fields = ('title', 'tasks')

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

