from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from tasklists.api_views import TaskListLCApiView
from .mixins import UserCategoryQuerysetMixin
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
