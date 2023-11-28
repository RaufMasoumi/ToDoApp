from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from .serializers import TaskDetailSerializer
from .mixins import UserTaskQuerysetMixin
from .filters import TaskFilterSet
from .forms import TASK_SEARCH_FIELDS, TASK_ORDERING_FIELDS


class TaskLCApiView(UserTaskQuerysetMixin, ListCreateAPIView):
    serializer_class = TaskDetailSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = TASK_SEARCH_FIELDS
    ordering_fields = TASK_ORDERING_FIELDS
    filterset_class = TaskFilterSet

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskRUDApiView(UserTaskQuerysetMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer


