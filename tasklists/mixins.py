from django.shortcuts import get_object_or_404
from .validators import validate_title
# Warning: Only use mixins as a parent class of proper child class, not as a dedicated class.


class UserTaskListQuerysetMixin:
    def __init__(self, request=None):
        self.request = request

    def get_queryset(self):
        return self.request.user.tasklists.all()


class DynamicTaskListTaskQuerysetMixin:

    def get_tasklist(self):
        user_tasklists = self.request.user.tasklists.all()
        tasklist = get_object_or_404(user_tasklists, slug=self.kwargs.get('tasklist'))
        return tasklist

    def get_queryset(self):
        return self.get_tasklist().tasks.all()


class TasksCountMixin:

    def get_tasks_count(self, obj):
        return obj.tasks.count()


class FormTitleValidationMixin:
    reverse_relation = 'tasklists'

    def clean_title(self):
        base_title = self.cleaned_data.get('title', None)
        if 'title' not in self.changed_data:
            return base_title
        title = validate_title(base_title, self.instance, getattr(self.user, self.reverse_relation, None))
        return title


class SerializerTitleValidationMixin:
    user_queryset_related_name = None

    def validate_title(self, value):
        title = validate_title(value, self.instance, getattr(self.request.user, self.user_queryset_related_name, None))
        return title
