from django.db.models import QuerySet
from rest_framework import serializers
from tasklists.nested_serializers import TaskListNestedSerializer
from tasklists.models import TaskList
from .models import Task


class TaskDetailSerializer(serializers.HyperlinkedModelSerializer):
    tasklists = TaskListNestedSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'url', 'user', 'title', 'due_date', 'is_done', 'is_important', 'is_not_important',
                  'is_timely_important', 'tasklists', 'created_at', 'updated_at', 'done_at']

        extra_kwargs = {
            'url': {'view_name': 'api-task-detail'},
            'user': {'view_name': 'api-user-detail', 'lookup_field': 'slug', 'read_only': True},
            'done_at': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data, tasklists = get_tasklists_from_data(validated_data)
        task = super().create(validated_data)
        task.tasklists.set(tasklists)
        task.save()
        return task

    def update(self, instance, validated_data):
        validated_data, tasklists = get_tasklists_from_data(validated_data)
        instance.tasklists.set(tasklists)
        return super().update(instance, validated_data)

    def validate(self, data):
        data = super().validate(data)
        if data['is_important']:
            data['is_not_important'] = False
        return data


def get_tasklists_from_data(validated_data: dict):
    tasklists = TaskList.objects.none()
    if validated_data.get('tasklists', None):
        tasklists_data = validated_data.pop('tasklists')
        tasklists_pk = [tasklist_data.get('pk') for tasklist_data in tasklists_data]
        tasklists = TaskList.objects.filter(pk__in=tasklists_pk)
        tasklists = tasklists.filter(user=validated_data['user'])
    return validated_data, tasklists
