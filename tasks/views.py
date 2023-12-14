from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.filters import SearchFilter, OrderingFilter
from .mixins import AllauthLoginRequiredMixin, UserTaskQuerysetMixin, ViewSOFMixin
from .forms import TaskModelForm, SearchForm, TaskOrderingForm, TASK_SEARCH_FIELDS
from .filters import TaskFilterSet
# Create your views here.


class TaskListView(AllauthLoginRequiredMixin, UserTaskQuerysetMixin, ViewSOFMixin, ListView):
    template_name = 'tasks/task_list.html'
    search_form = SearchForm
    search_filter_class = SearchFilter
    search_fields = TASK_SEARCH_FIELDS
    ordering_form = TaskOrderingForm
    ordering_filter_class = OrderingFilter
    ordering_fields = ordering_form.ordering_fields
    filterset_class = TaskFilterSet


class TaskDetailView(AllauthLoginRequiredMixin, UserTaskQuerysetMixin, DetailView):
    template_name = 'tasks/task_detail.html'


class TaskCreateView(AllauthLoginRequiredMixin, CreateView):
    form_class = TaskModelForm
    template_name = 'tasks/task_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AllauthLoginRequiredMixin, UserTaskQuerysetMixin, UpdateView):
    form_class = TaskModelForm
    template_name = 'tasks/task_update.html'


class TaskDeleteView(AllauthLoginRequiredMixin, UserTaskQuerysetMixin, DeleteView):
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('task-list')
