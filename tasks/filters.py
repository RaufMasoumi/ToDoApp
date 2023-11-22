from django_filters.rest_framework.filterset import FilterSet
from .models import Task


class TaskFilterSet(FilterSet):
    class Meta:
        model = Task
        fields = {
            'title': ['iexact', 'icontains'],
            'due_date': ['exact', 'month', 'month__gt', 'year', 'year__gt'],
            'is_done': ['exact'],
            'is_important': ['exact'],
            'is_timely_important': ['exact'],
            'is_not_important': ['exact'],
            'created_at': ['exact', 'month', 'month__gt', 'year', 'year__gt'],
            'updated_at': ['exact', 'month', 'month__gt', 'year', 'year__gt'],
            'done_at': ['exact', 'month', 'month__gt', 'year', 'year__gt']
        }


TASK_FILTERSETS_LIST = [TaskFilterSet, ]
