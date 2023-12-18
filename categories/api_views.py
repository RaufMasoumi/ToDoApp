from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from tasklists.api_views import TaskListLCApiView
from tasks.serializers import TaskDetailSerializer
from tasks.forms import TASK_SEARCH_FIELDS, TASK_ORDERING_FIELDS
from tasks.filters import TaskFilterSet
from .mixins import UserCategoryQuerysetMixin, DynamicCategoryTaskQuerysetMixin
from .serializers import CategoryListSerializer, CategoryDetailSerializer
from .filters import CategoryFilterSet
from .forms import CATEGORY_SEARCH_FIELDS, CATEGORY_ORDERING_FIELDS


class CategoryLCApiView(UserCategoryQuerysetMixin, TaskListLCApiView):
    serializer_class = CategoryListSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = CATEGORY_SEARCH_FIELDS
    ordering_fields = CATEGORY_ORDERING_FIELDS
    filterset_class = CategoryFilterSet


class CategoryRUDApiView(UserCategoryQuerysetMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CategoryTaskLCApiView(DynamicCategoryTaskQuerysetMixin, ListCreateAPIView):
    serializer_class = TaskDetailSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = TASK_SEARCH_FIELDS
    ordering_fields = TASK_ORDERING_FIELDS
    filterset_class = TaskFilterSet

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, categories={self.get_category()})


class CategoryTaskDestroyApiView(DynamicCategoryTaskQuerysetMixin, DestroyAPIView):
    serializer_class = TaskDetailSerializer

    def perform_destroy(self, instance):
        instance.categories.remove(self.get_category())
