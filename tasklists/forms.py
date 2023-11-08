from django.forms import ModelForm
from django.utils.text import slugify
from .models import TaskList


class TaskListModelForm(ModelForm):

    class Meta:
        model = TaskList
        fields = ('title', 'tasks')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        base_title = self.cleaned_data.get('title')
        if 'title' not in self.changed_data:
            return base_title
        slug = slugify(base_title)
        matching_tasklists_slugs = self.request.user.tasklists.filter(slug__startswith=slug).values_list(
            'slug', flat=True
        )
        if self.instance:
            matching_tasklists_slugs = matching_tasklists_slugs.exclude(pk=self.instance.pk)
        number = 0
        title = base_title
        while slugify(title) in matching_tasklists_slugs:
            number += 1
            title = f'{base_title}({number})'
        return title

