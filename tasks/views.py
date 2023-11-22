from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .mixins import AllauthLoginRequiredMixin, UserTaskQuerysetMixin
from .forms import TaskModelForm
from .filters import TaskFilterSet
# Create your views here.


class TaskListView(AllauthLoginRequiredMixin, UserTaskQuerysetMixin, ListView):
    template_name = 'tasks/task_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TaskFilterSet(self.request.GET, self.get_queryset())
        return context


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

    def get_success_url(self):
        success_url = self.success_url
        get = self.request.GET
        if get.get('tasklist'):
            tasklist = self.request.user.tasklists.get(slug=get['tasklist'])
            success_url = tasklist.get_absolute_url()
        return success_url
