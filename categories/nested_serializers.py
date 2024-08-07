from rest_framework import serializers
from categories.models import Category


class CategoryNestedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'title')
        extra_kwargs = {
            'url': {'view_name': 'api-category-detail', 'lookup_field': 'slug'}
        }
