from django_filters.rest_framework.filterset import FilterSet
from tasks.filters import TASK_FILTERSETS_LIST
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
FILTERSETS_LIST = TASKLIST_FILTERSETS_LIST + TASK_FILTERSETS_LIST

ALL_FILTERSETS_FIELD_NAMES = []
for filterset in FILTERSETS_LIST:
    for field_name, lookup_exprs in filterset.get_fields().items():
        for lookup_expr in lookup_exprs:
            ALL_FILTERSETS_FIELD_NAMES.append(filterset.get_filter_name(field_name, lookup_expr))
