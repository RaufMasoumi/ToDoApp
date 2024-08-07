from django import forms
from django.forms import ModelForm
from .models import Task

TASK_SEARCH_FIELDS = ['title', ]
TASK_ORDERING_FIELDS = ['title', 'due_date', 'is_done', 'is_important', 'created_at', 'updated_at', 'done_at']


class TaskModelForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'due_date', 'categories', 'is_daily', 'is_important', 'is_not_important', 'is_timely_important', 'is_done'
        ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['is_important']:
            cleaned_data['is_not_important'] = False
        return cleaned_data


class SearchForm(forms.Form):
    search = forms.CharField(max_length=300, required=False)


def get_ordering_choices(ordering_fields):
    choices = ()
    for ordering_field in ordering_fields:
        ascending_field = (ordering_field, f'{ordering_field}_Ascending')
        descending_field = (f'-{ordering_field}', f'{ordering_field}_Descending')
        choices += (ascending_field, ) + (descending_field, )
    return choices


class TaskOrderingForm(forms.Form):
    ordering_fields = TASK_ORDERING_FIELDS
    ORDERING_CHOICES = get_ordering_choices(ordering_fields)
    ordering = forms.ChoiceField(choices=ORDERING_CHOICES, required=False)


