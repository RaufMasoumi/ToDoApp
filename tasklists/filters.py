from django_filters.rest_framework.filterset import FilterSet
from .models import TaskList


class TaskListFilterSet(FilterSet):
    class Meta:
        model = TaskList
        fields = {
            'title': ['iexact', 'icontains'],
            'created_at': ['exact', 'month', 'month__gt', 'year', 'year__gt'],
            'updated_at': ['exact', 'month', 'month__gt', 'year', 'year__gt'],
            'tasks__title': ['icontains']
        }

    @property
    def qs(self):
        parent = super().qs
        return parent.distinct()


TASKLIST_FILTERSETS_LIST = [TaskListFilterSet, ]
