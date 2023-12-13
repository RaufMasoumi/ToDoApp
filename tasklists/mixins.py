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


class FormInitAdditionalDataMixin:

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


class FormTitleValidationMixin(FormInitAdditionalDataMixin):
    reverse_relation = 'tasklists'

    def clean_title(self):
        base_title = self.cleaned_data.get('title', None)
        if 'title' not in self.changed_data:
            return base_title
        title = validate_title(base_title, self.instance, getattr(self.user, self.reverse_relation, None))
        return title


class SerializerInitAdditionalDataMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request', None)
        self.instance_user = self.context.get('instance_user', None)
        if hasattr(self.context.get('instance', None), 'user'):
            self.user = self.context['instance'].user
        elif self.instance_user:
            self.user = self.instance_user
        else:
            self.user = self.request.user


class SerializerTitleValidationMixin(SerializerInitAdditionalDataMixin):

    def validate_title(self, value):
        title = validate_title(value, self.instance, self.user.tasklists)
        return title
