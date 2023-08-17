from rest_framework import serializers
from .models import Task


class TaskDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'api-task-detail'},
            'user': {'view_name': 'api-user-detail', 'lookup_field': 'slug', 'read_only': True},
            'done_at': {'read_only': True},
        }


class TaskNestedSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-task-detail')
    title = serializers.CharField(max_length=300)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
