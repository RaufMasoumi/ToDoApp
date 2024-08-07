from rest_framework import serializers
from tasklists.nested_serializers import TaskListNestedSerializer
from tasklists.models import TaskList
from categories.nested_serializers import CategoryNestedSerializer
from .models import Task


class TaskDetailSerializer(serializers.HyperlinkedModelSerializer):
    tasklists = TaskListNestedSerializer(many=True, required=False)
    categories = CategoryNestedSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'url', 'user', 'title', 'due_date', 'is_daily', 'is_done', 'is_important', 'is_not_important',
                  'is_timely_important', 'tasklists', 'categories', 'created_at', 'updated_at', 'done_at']

        extra_kwargs = {
            'url': {'view_name': 'api-task-detail'},
            'user': {'view_name': 'api-user-detail', 'lookup_field': 'slug', 'read_only': True},
            'done_at': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data, tasklists = get_tasklists_from_data(validated_data)
        task = super().create(validated_data)
        task.tasklists.set(task.tasklists.default_tasklists() | tasklists)
        task.save()
        return task

    def update(self, instance, validated_data):
        validated_data, tasklists = get_tasklists_from_data(validated_data, instance)
        task = super().update(instance, validated_data)
        task.tasklists.set(task.tasklists.default_tasklists() | tasklists)
        task.save()
        return task

    def validate(self, data):
        data = super().validate(data)
        if data.get('is_important', None):
            data['is_not_important'] = False
        return data


def get_tasklists_from_data(validated_data: dict, instance=None):
    tasklists = TaskList.objects.none()
    if validated_data.get('tasklists', None):
        user = instance.user if instance else validated_data.get('user', None)
        tasklists_data = validated_data.pop('tasklists')
        tasklists_pk = [tasklist_data.get('pk') for tasklist_data in tasklists_data]
        tasklists = TaskList.objects.filter(pk__in=tasklists_pk, user=user)
    return validated_data, tasklists
