from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from tasks.serializers import TaskDetailSerializer
from .serializers import TaskListListSerializer, TaskListDetailSerializer
from .mixins import UserTaskListQuerysetMixin, DynamicTaskListTaskQuerysetMixin
from tasks.models import add_task_to_tasklist, remove_task_from_tasklist
from .permissions import DefaultTaskListPermission, TaskDefaultTaskListPermission


class TaskListLCApiView(UserTaskListQuerysetMixin, ListCreateAPIView):
    serializer_class = TaskListListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListRUDApiView(UserTaskListQuerysetMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = TaskListDetailSerializer
    permission_classes = [IsAuthenticated, DefaultTaskListPermission]


class TaskListTaskLCApiView(DynamicTaskListTaskQuerysetMixin, ListCreateAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated, TaskDefaultTaskListPermission]

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        add_task_to_tasklist(self.get_tasklist(), instance)


class TaskListTaskDestroyApiView(DynamicTaskListTaskQuerysetMixin, DestroyAPIView):
    permission_classes = [IsAuthenticated, TaskDefaultTaskListPermission]

    def perform_destroy(self, instance):
        remove_task_from_tasklist(self.get_tasklist(), instance)

