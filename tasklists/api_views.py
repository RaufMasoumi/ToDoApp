from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from tasks.serializers import TaskDetailSerializer
from tasks.models import add_task_to_tasklist, remove_task_from_tasklist
from tasks.filters import TaskFilterSet
from .serializers import TaskListListSerializer, TaskListDetailSerializer
from .mixins import UserTaskListQuerysetMixin, DynamicTaskListTaskQuerysetMixin
from .permissions import DefaultTaskListPermission, TaskDefaultTaskListPermission
from .filters import TaskListFilterSet
from .forms import TASKLIST_SEARCH_FIELDS, TASKLIST_ORDERING_FIELDS


class TaskListLCApiView(UserTaskListQuerysetMixin, ListCreateAPIView):
    serializer_class = TaskListListSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = TASKLIST_SEARCH_FIELDS
    ordering_fields = TASKLIST_ORDERING_FIELDS
    filterset_class = TaskListFilterSet

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['instance_user'] = self.request.user
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListRUDApiView(UserTaskListQuerysetMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = TaskListDetailSerializer
    permission_classes = [IsAuthenticated, DefaultTaskListPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class TaskListTaskLCApiView(DynamicTaskListTaskQuerysetMixin, ListCreateAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated, TaskDefaultTaskListPermission]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TaskFilterSet

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        add_task_to_tasklist(self.get_tasklist(), instance)


class TaskListTaskDestroyApiView(DynamicTaskListTaskQuerysetMixin, DestroyAPIView):
    permission_classes = [IsAuthenticated, TaskDefaultTaskListPermission]

    def perform_destroy(self, instance):
        remove_task_from_tasklist(self.get_tasklist(), instance)

