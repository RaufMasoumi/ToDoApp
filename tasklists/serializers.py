from rest_framework import serializers
from tasks.nested_serializers import TaskNestedSerializer
from .models import TaskList


class TaskListListSerializer(serializers.HyperlinkedModelSerializer):
    tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = TaskList
        fields = ['id', 'url', 'user', 'title', 'slug', 'tasks_count', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'user']
        extra_kwargs = {
            'url': {'view_name': 'api-tasklist-detail', 'lookup_field': 'slug'},
            'user': {'view_name': 'api-user-detail', 'lookup_field': 'slug'}
        }

    def get_tasks_count(self, obj):
        return obj.tasks.count()


class TaskListDetailSerializer(serializers.HyperlinkedModelSerializer):
    tasks = TaskNestedSerializer(many=True, read_only=True)

    class Meta:
        model = TaskList
        fields = ['id', 'url', 'user', 'title', 'slug', 'tasks', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'user']
        extra_kwargs = {
            'url': {'view_name': 'api-tasklist-detail', 'lookup_field': 'slug'},
            'user': {'view_name': 'api-user-detail', 'lookup_field': 'slug'}
        }


