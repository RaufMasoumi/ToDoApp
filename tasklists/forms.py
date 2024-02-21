from django import forms
from django.forms import ModelForm
from tasks.forms import get_ordering_choices
from .models import TaskList
from .mixins import FormTitleValidationMixin

TASKLIST_SEARCH_FIELDS = ['title', ]
TASKLIST_ORDERING_FIELDS = ['title', 'created_at', 'updated_at']


class CustomModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.instance_user = kwargs.pop('instance_user', None)
        super().__init__(*args, **kwargs)
        if hasattr(self.instance, 'user'):
            self.user = self.instance.user
        elif self.instance_user:
            self.user = self.instance_user
        else:
            self.user = self.request.user


class TaskListModelForm(FormTitleValidationMixin, CustomModelForm):
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
