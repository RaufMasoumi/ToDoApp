from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from rest_framework.filters import SearchFilter
from tasks.views import TaskUpdateView
from tasks.mixins import AllauthLoginRequiredMixin
from tasks.models import add_task_to_tasklist, remove_task_from_tasklist
from tasks.forms import TaskModelForm, SearchForm
from tasks.filters import TaskFilterSet
from .mixins import UserTaskListQuerysetMixin, DynamicTaskListTaskQuerysetMixin
from .permissions import DefaultTaskListPermissionMixin
from .models import TaskList
from .forms import TaskListModelForm, TaskListOrderingForm
from .filters import TaskListFilterSet
# Create your views here.


class TaskListListView(AllauthLoginRequiredMixin, UserTaskListQuerysetMixin, ListView):
    context_object_name = 'tasklists'
    template_name = 'tasklists/tasklist_list.html'
    search_fields = ['title', ]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        queryset = self.get_queryset()
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)
        self.request.query_params = self.request.GET
        search_filter = SearchFilter()
        queryset = search_filter.filter_queryset(self.request, queryset, self)
        context['filter'] = TaskListFilterSet(self.request.GET, queryset)
        context['search_form'] = SearchForm(self.request.GET)
        context['ordering_form'] = TaskListOrderingForm(self.request.GET)
        return context

    def get_ordering(self):
        ordering_form = TaskListOrderingForm(self.request.GET)
        if ordering_form.is_valid():
            return ordering_form.cleaned_data['ordering']
        return None


class TaskListDetailView(AllauthLoginRequiredMixin, UserTaskListQuerysetMixin, DetailView):
    template_name = 'tasklists/tasklist_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_filter'] = TaskFilterSet(self.request.GET, self.get_object().tasks.all())
        return context


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
        kwargs['instance_user'] = self.get_object().user
        return kwargs


class TaskListDeleteView(AllauthLoginRequiredMixin, DefaultTaskListPermissionMixin, UserTaskListQuerysetMixin, DeleteView):
    template_name = 'tasklists/tasklist_delete.html'
    success_url = reverse_lazy('tasklist-list')


class TaskListTaskCreateView(AllauthLoginRequiredMixin, DefaultTaskListPermissionMixin, CreateView):
    template_name = 'tasks/task_create.html'
    form_class = TaskModelForm

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
            return tasklist.get_absolute_url()


class TaskListTaskDeleteView(AllauthLoginRequiredMixin, DefaultTaskListPermissionMixin, DynamicTaskListTaskQuerysetMixin, DeleteView):
    template_name = 'tasks/task_delete.html'
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
