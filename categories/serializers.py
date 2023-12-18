from rest_framework import serializers
from tasklists.serializers import BaseTaskListSerializer
from tasklists.mixins import TasksCountMixin
from tasks.nested_serializers import TaskNestedSerializer
from .models import Category


class BaseCategorySerializer(BaseTaskListSerializer):
    user_queryset_related_name = 'categories'

    class Meta(BaseTaskListSerializer.Meta):
        model = Category
        extra_kwargs = BaseTaskListSerializer.Meta.extra_kwargs.copy()
        extra_kwargs.update({
            'url': {'view_name': 'api-category-detail', 'lookup_field': 'slug'},
        })


class CategoryListSerializer(TasksCountMixin, BaseCategorySerializer):
    tasks_count = serializers.SerializerMethodField()

    class Meta(BaseCategorySerializer.Meta):
        fields = ['id', 'url', 'user', 'title', 'slug', 'tasks_count', 'created_at', 'updated_at']


class CategoryDetailSerializer(BaseCategorySerializer):
    tasks = TaskNestedSerializer(many=True, read_only=True)

    class Meta(BaseCategorySerializer.Meta):
        fields = ['id', 'url', 'user', 'title', 'slug', 'tasks', 'created_at', 'updated_at']

