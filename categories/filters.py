from tasklists.filters import TaskListFilterSet
from .models import Category


class CategoryFilterSet(TaskListFilterSet):
    class Meta(TaskListFilterSet.Meta):
        model = Category


CATEGORY_FILTERSETS_LIST = [CategoryFilterSet, ]
