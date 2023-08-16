from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from tasks.views import AllauthLoginRequiredMixin, TaskUpdateView
from tasks.models import Task
from .models import TaskList
# Create your views here.


class TaskListUserQuerysetMixin:
    request = None

    def get_queryset(self):
        return TaskList.objects.user_tasklist(user=self.request.user)


class TaskListListView(AllauthLoginRequiredMixin, TaskListUserQuerysetMixin, ListView):
    context_object_name = 'tasklists'
    template_name = 'tasklists/tasklist_list.html'


class TaskListDetailView(AllauthLoginRequiredMixin, TaskListUserQuerysetMixin, DetailView):
    template_name = 'tasklists/tasklist_detail.html'


class TaskListCreateView(AllauthLoginRequiredMixin, CreateView):
    model = TaskList
    template_name = 'tasklists/tasklist_create.html'
    fields = ('title', 'tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskListUpdateView(AllauthLoginRequiredMixin, TaskListUserQuerysetMixin, UpdateView):
    template_name = 'tasklists/tasklist_update.html'
    fields = ('title', 'tasks')


class TaskListDeleteView(AllauthLoginRequiredMixin, TaskListUserQuerysetMixin, DeleteView):
    template_name = 'tasklists/tasklist_delete.html'

    def get_success_url(self):
        return reverse('tasklist-list')


class TaskListTaskCreateView(AllauthLoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasklists/tasklist_task_create.html'
    fields = ('title', 'due_date', 'is_important', 'is_not_important', 'is_timely_important')

    def get_object(self, queryset=None):
        queryset = TaskList.objects.user_tasklist(self.request.user)
        self.slug_url_kwarg = 'tasklist'
        return super().get_object(queryset=queryset)

    def form_valid(self, form):
        form.instance.user = self.request.user
        task = self.object = form.save()
        tasklist = self.get_object()
        tasklist.tasks.add(task)
        tasklist.save()
        return HttpResponseRedirect(tasklist.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasklist'] = self.get_object()
        return context


class TaskListTaskUpdateView(TaskUpdateView):
    def get_success_url(self):
        success_url = self.success_url
        if self.kwargs.get('tasklist'):
            try:
                tasklist = TaskList.objects.get(slug=self.kwargs['tasklist'])
            except TaskList.DoesNotExist:
                pass
            else:
                success_url = tasklist.get_absolute_url()
        return success_url
