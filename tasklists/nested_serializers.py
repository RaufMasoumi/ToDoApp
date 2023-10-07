from rest_framework import serializers
from .models import TaskList


class TaskListNestedSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-tasklist-detail', lookup_field='slug')
    pk = serializers.UUIDField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
