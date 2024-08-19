from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
from .mixins import AllauthLoginRequiredMixin, UserTaskQuerysetMixin, ViewSOFMixin
from .forms import TaskModelForm, SearchForm, TaskOrderingForm, TASK_SEARCH_FIELDS
from .filters import TaskFilterSet
from .models import TaskStep


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


class TaskStepCreateView(AllauthLoginRequiredMixin, UserPassesTestMixin, CreateView):
    queryset = TaskStep.objects.all()
    fields = ('title', 'is_done')
    template_name = 'tasks/taskstep_create.html'

    def dispatch(self, request, *args, **kwargs):
        user_tasks = request.user.tasks.all()
        task_pk = request.GET.get('task', None)
        self.task = get_object_or_404(user_tasks, pk=task_pk)
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.task.user == self.request.user

    def form_valid(self, form):
        form.instance.task = self.task
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.task.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        return context


class TaskStepUpdateView(AllauthLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    queryset = TaskStep.objects.all()
    fields = ('title', 'is_done', )
    template_name = 'tasks/taskstep_update.html'

    def test_func(self):
        obj = self.get_object()
        return obj.task.user == self.request.user

    def get_success_url(self):
        return self.object.task.get_absolute_url()


class TaskStepDeleteView(AllauthLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    queryset = TaskStep.objects.all()
    template_name = 'tasks/taskstep_delete.html'

    def test_func(self):
        obj = self.get_object()
        return obj.task.user == self.request.user

    def get_success_url(self):
        return self.object.task.get_absolute_url()

