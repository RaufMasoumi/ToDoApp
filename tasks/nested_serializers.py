from rest_framework import serializers


class TaskNestedSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='api-task-detail')
    title = serializers.CharField(max_length=300)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
