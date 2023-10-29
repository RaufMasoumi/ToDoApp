from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from tasks.views import TaskUpdateView, TASK_FIELDS
from tasks.mixins import AllauthLoginRequiredMixin
from tasks.models import Task, add_task_to_tasklist, remove_task_from_tasklist
from .mixins import UserTaskListQuerysetMixin, DynamicTaskListTaskQuerysetMixin
from .permissions import DefaultTaskListPermissionMixin
from .models import TaskList
# Create your views here.


class TaskListListView(AllauthLoginRequiredMixin, UserTaskListQuerysetMixin, ListView):
    context_object_name = 'tasklists'
    template_name = 'tasklists/tasklist_list.html'


class TaskListDetailView(AllauthLoginRequiredMixin, UserTaskListQuerysetMixin, DetailView):
    template_name = 'tasklists/tasklist_detail.html'


class TaskListCreateView(AllauthLoginRequiredMixin, CreateView):
    model = TaskList
    template_name = 'tasklists/tasklist_create.html'
    fields = ('title', 'tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskListUpdateView(AllauthLoginRequiredMixin, DefaultTaskListPermissionMixin, UserTaskListQuerysetMixin, UpdateView):
    template_name = 'tasklists/tasklist_update.html'
    fields = ('title', 'tasks')


class TaskListDeleteView(AllauthLoginRequiredMixin, DefaultTaskListPermissionMixin, UserTaskListQuerysetMixin, DeleteView):
    template_name = 'tasklists/tasklist_delete.html'
    success_url = reverse_lazy('tasklist-list')


class TaskListTaskCreateView(AllauthLoginRequiredMixin, DefaultTaskListPermissionMixin, CreateView):
    model = Task
    template_name = 'tasks/task_create.html'
    fields = TASK_FIELDS

    def get_object(self, queryset=None):
        mixin = UserTaskListQuerysetMixin(self.request)
        queryset = mixin.get_queryset()
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
            tasklist = self.request.user.tasklists.get(slug=self.kwargs['tasklist'])
        except TaskList.DoesNotExist:
            return super().get_success_url()
        else:
            success_url = tasklist.get_absolute_url()
            return success_url


class TaskListTaskDeleteView(AllauthLoginRequiredMixin, DefaultTaskListPermissionMixin, DynamicTaskListTaskQuerysetMixin, DeleteView):
    template_name = 'tasks/task_delete.html'
    tasklist_getter = 'get_tasklist'

    def get_success_url(self):
        return self.get_tasklist().get_absolute_url()

    def form_valid(self, form=None):
        tasklist = remove_task_from_tasklist(self.get_tasklist(), self.get_object())
        return HttpResponseRedirect(tasklist.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasklist'] = self.get_tasklist()
        return context
