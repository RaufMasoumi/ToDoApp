from rest_framework import serializers
from tasks.nested_serializers import TaskNestedSerializer
from .mixins import TasksCountMixin, SerializerTitleValidationMixin
from .models import TaskList


class CustomHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
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


class BaseTaskListSerializer(SerializerTitleValidationMixin, CustomHyperlinkedModelSerializer):
    user_queryset_related_name = 'tasklists'

    class Meta:
        model = TaskList
        fields = ['id', 'url', 'user', 'title', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'user']
        extra_kwargs = {
            'url': {'view_name': 'api-tasklist-detail', 'lookup_field': 'slug'},
            'user': {'view_name': 'api-user-detail', 'lookup_field': 'slug'}
        }


class TaskListListSerializer(TasksCountMixin, BaseTaskListSerializer):
    tasks_count = serializers.SerializerMethodField()

    class Meta(BaseTaskListSerializer.Meta):
        fields = ['id', 'url', 'user', 'title', 'slug', 'tasks_count', 'created_at', 'updated_at']


class TaskListDetailSerializer(BaseTaskListSerializer):
    tasks = TaskNestedSerializer(many=True, read_only=True)

    class Meta(BaseTaskListSerializer.Meta):
        fields = ['id', 'url', 'user', 'title', 'slug', 'tasks', 'created_at', 'updated_at']


