from django.shortcuts import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from tasks.views import AllauthLoginRequiredMixin, TaskUpdateView
from tasks.models import Task
from .mixins import TaskListUserQuerysetMixin, DynamicTaskListTaskQuerysetMixin
from .models import TaskList
# Create your views here.


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
        queryset = self.request.user.tasklists.all()
        self.slug_url_kwarg = 'tasklist'
        return super().get_object(queryset=queryset)

    def form_valid(self, form):
        form.instance.user = self.request.user
        task = self.object = form.save()
        tasklist = add_task_to_tasklist(self.get_object(), task)
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


class TaskListTaskDeleteView(AllauthLoginRequiredMixin, DynamicTaskListTaskQuerysetMixin, DeleteView):
    template_name = 'tasks/task_delete.html'

    def get_success_url(self):
        return self.get_tasklist().get_absolute_url()

    def form_valid(self, form=None):
        tasklist = remove_task_from_tasklist(self.get_tasklist(), self.get_object())
        return HttpResponseRedirect(tasklist.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasklist'] = self.get_tasklist()
        return context


def add_task_to_tasklist(tasklist, task):
    tasklist.tasks.add(task)
    tasklist.save()
    return tasklist


def remove_task_from_tasklist(tasklist, task):
    tasklist.tasks.remove(task)
    tasklist.save()
    return tasklist
