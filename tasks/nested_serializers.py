from rest_framework import serializers
from .models import Task


class TaskNestedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        fields = ['url', 'id', 'title']
        extra_kwargs = {
            'url': {'view_name': 'api-task-detail'},
            'title': {'required': False}
        }
