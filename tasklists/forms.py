from django import forms
from tasks.forms import TaskOrderingForm
from .models import TaskList
from .mixins import FormTitleValidationMixin

TASKLIST_SEARCH_FIELDS = ['title', ]
TASKLIST_ORDERING_FIELDS = ['title', 'created_at', 'updated_at']


class TaskListModelForm(FormTitleValidationMixin, forms.ModelForm):

    class Meta:
        model = TaskList
        fields = ('title', 'tasks')

    def clean_tasks(self):
        tasks = self.cleaned_data.get('tasks')
        tasks = tasks.filter(user=self.user)
        return tasks


class TaskListOrderingForm(TaskOrderingForm):
    ordering_fields = TASKLIST_ORDERING_FIELDS
