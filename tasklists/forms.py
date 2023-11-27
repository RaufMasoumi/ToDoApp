from django import forms
from django.utils.text import slugify
from .models import TaskList


class TaskListModelForm(forms.ModelForm):

    class Meta:
        model = TaskList
        fields = ('title', 'tasks')

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

    def clean_title(self):
        base_title = self.cleaned_data.get('title')
        if 'title' not in self.changed_data:
            return base_title
        title = validate_title(base_title, self.instance, self.user)
        return title

    def clean_tasks(self):
        tasks = self.cleaned_data.get('tasks')
        tasks = tasks.filter(user=self.user)
        return tasks


class TaskListOrderingForm(forms.Form):
    ordering_fields = ['title', 'created_at', 'updated_at']
    ORDERING_CHOICES = ()
    for ordering_field in ordering_fields:
        ascending_field = (ordering_field, f'{ordering_field}_Ascending')
        descending_field = (f'-{ordering_field}', f'{ordering_field}_Descending')
        ORDERING_CHOICES += (ascending_field, ) + (descending_field, )
    ordering = forms.ChoiceField(choices=ORDERING_CHOICES, required=False)


def validate_title(base_title, instance, user):
    slug = slugify(base_title)
    matching_tasklists_slugs = user.tasklists.filter(slug__startswith=slug).values_list(
        'slug', flat=True
    )
    if instance:
        matching_tasklists_slugs = matching_tasklists_slugs.exclude(pk=instance.pk)
    number = 0
    title = base_title
    while slugify(title) in matching_tasklists_slugs:
        number += 1
        title = f'{base_title}({number})'
    return title
