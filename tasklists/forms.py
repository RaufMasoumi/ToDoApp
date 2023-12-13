from django import forms
from tasks.forms import get_ordering_choices
from .models import TaskList
from .mixins import FormTitleValidationMixin

TASKLIST_SEARCH_FIELDS = ['title', ]
TASKLIST_ORDERING_FIELDS = ['title', 'created_at', 'updated_at']


class TaskListModelForm(FormTitleValidationMixin, forms.ModelForm):
    reverse_relation = 'tasklists'

    class Meta:
        model = TaskList
        fields = ('title', 'tasks')

    def clean_tasks(self):
        tasks = self.cleaned_data.get('tasks')
        tasks = tasks.filter(user=self.user)
        return tasks


class TaskListOrderingForm(forms.Form):
    ordering_fields = TASKLIST_ORDERING_FIELDS
    ORDERING_CHOICES = get_ordering_choices(ordering_fields)
    ordering = forms.ChoiceField(choices=ORDERING_CHOICES, required=False)