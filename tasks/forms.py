from django.forms import ModelForm
from .models import Task


class TaskModelForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'due_date', 'is_daily', 'is_important', 'is_not_important', 'is_timely_important', 'is_done'
        ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['is_important']:
            cleaned_data['is_not_important'] = False
        return cleaned_data
