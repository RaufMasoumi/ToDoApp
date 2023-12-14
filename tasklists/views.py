from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from rest_framework.filters import SearchFilter, OrderingFilter
from tasks.views import TaskUpdateView
from tasks.mixins import AllauthLoginRequiredMixin, ViewSOFMixin
from tasks.models import add_task_to_tasklist, remove_task_from_tasklist
from tasks.forms import TaskModelForm, SearchForm, TaskOrderingForm, TASK_SEARCH_FIELDS
from tasks.filters import TaskFilterSet
from .mixins import UserTaskListQuerysetMixin, DynamicTaskListTaskQuerysetMixin
from .permissions import DefaultTaskListPermissionMixin
from .models import TaskList
from .forms import TaskListModelForm, TaskListOrderingForm, TASKLIST_SEARCH_FIELDS
from .filters import TaskListFilterSet
# Create your views here.


class TaskListListView(AllauthLoginRequiredMixin, UserTaskListQuerysetMixin, ViewSOFMixin, ListView):
    context_object_name = 'tasklists'
    template_name = 'tasklists/tasklist_list.html'
    search_form = SearchForm
    search_filter_class = SearchFilter
    search_fields = TASKLIST_SEARCH_FIELDS
    ordering_form = TaskListOrderingForm
    ordering_filter_class = OrderingFilter
    ordering_fields = ordering_form.ordering_fields
    filterset_class = TaskListFilterSet


class TaskListDetailView(AllauthLoginRequiredMixin, UserTaskListQuerysetMixin, ViewSOFMixin, DetailView):
    template_name = 'tasklists/tasklist_detail.html'
    search_form = SearchForm
    search_filter_class = SearchFilter
    search_fields = TASK_SEARCH_FIELDS
    ordering_form = TaskOrderingForm
    ordering_filter_class = OrderingFilter
    ordering_fields = ordering_form.ordering_fields
    filterset_class = TaskFilterSet

    def get_filter_queryset(self):
        return self.get_object().tasks.all()


class TaskListCreateView(AllauthLoginRequiredMixin, CreateView):
    model = TaskList
    template_name = 'tasklists/tasklist_create.html'
    form_class = TaskListModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['instance_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskListUpdateView(AllauthLoginRequiredMixin, DefaultTaskListPermissionMixin, UserTaskListQuerysetMixin, UpdateView):
    template_name = 'tasklists/tasklist_update.html'
    form_class = TaskListModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class TaskListDeleteView(AllauthLoginRequiredMixin, DefaultTaskListPermissionMixin, UserTaskListQuerysetMixin, DeleteView):
    template_name = 'tasklists/tasklist_delete.html'
    success_url = reverse_lazy('tasklist-list')


class TaskListTaskCreateView(AllauthLoginRequiredMixin, DefaultTaskListPermissionMixin, DynamicTaskListTaskQuerysetMixin, CreateView):
    template_name = 'tasklists/tasklist_task_create.html'
    form_class = TaskModelForm
    tasklist_getter = 'get_tasklist'

    def form_valid(self, form):
        form.instance.user = self.request.user
        task = self.object = form.save()
        tasklist = add_task_to_tasklist(self.get_tasklist(), task)
        return HttpResponseRedirect(tasklist.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasklist'] = self.get_tasklist()
        return context


class TaskListTaskUpdateView(TaskUpdateView):
    def get_success_url(self):
        try:
            tasklist = self.request.user.tasklists.get(slug=self.kwargs['tasklist'])
        except TaskList.DoesNotExist:
            return super().get_success_url()
        else:
            return tasklist.get_absolute_url()


class TaskListTaskDeleteView(AllauthLoginRequiredMixin, DefaultTaskListPermissionMixin, DynamicTaskListTaskQuerysetMixin, DeleteView):
    template_name = 'tasklists/tasklist_task_delete.html'
    tasklist_getter = 'get_tasklist'

    def get_success_url(self):
        return self.get_tasklist().get_absolute_url()

    def form_valid(self, form=None):
        remove_task_from_tasklist(self.get_tasklist(), self.get_object())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasklist'] = self.get_tasklist()
        return context
