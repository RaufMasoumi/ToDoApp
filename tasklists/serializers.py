from rest_framework import serializers
from tasks.nested_serializers import TaskNestedSerializer
from .mixins import TasksCountMixin, SerializerTitleValidationMixin
from .models import TaskList


class BaseTaskListSerializer(SerializerTitleValidationMixin, serializers.HyperlinkedModelSerializer):
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

