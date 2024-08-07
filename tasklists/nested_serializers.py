from rest_framework import serializers
from .models import TaskList


class TaskListNestedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskList
        fields = ('url', 'title', )
        extra_kwargs = {
            'url': {'view_name': 'api-tasklist-detail', 'lookup_field': 'slug'}
        }
