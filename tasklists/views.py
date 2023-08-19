from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from tasks.views import AllauthLoginRequiredMixin, UserTaskQuerysetMixin, TaskUpdateView
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
    template_name = 'tasks/task_create.html'
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
        try:
            tasklist = TaskList.objects.get(slug=self.kwargs['tasklist'])
        except TaskList.DoesNotExist:
            return super().get_success_url()
        else:
            success_url = tasklist.get_absolute_url()
            return success_url


class TaskListTaskDeleteView(AllauthLoginRequiredMixin, DeleteView):
    template_name = 'tasks/task_delete.html'

    def get_tasklist(self):
        tasklist_queryset = TaskList.objects.user_tasklist(self.request.user)
        tasklist = get_object_or_404(tasklist_queryset, slug=self.kwargs.get('tasklist'))
        return tasklist

    def get_queryset(self):
        return self.get_tasklist().tasks.all()

    def form_valid(self, form):
        tasklist = self.get_tasklist()
        tasklist.tasks.remove(self.get_object())
        tasklist.save()
        return HttpResponseRedirect(tasklist.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasklist'] = self.get_tasklist()
        return context
