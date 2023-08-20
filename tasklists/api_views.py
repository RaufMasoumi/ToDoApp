from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, DestroyAPIView
from tasks.serializers import TaskDetailSerializer
from .serializers import TaskListListSerializer, TaskListDetailSerializer
from .mixins import TaskListUserQuerysetMixin, DynamicTaskListTaskQuerysetMixin
from .views import add_task_to_tasklist, remove_task_from_tasklist


class TaskListLCApiView(TaskListUserQuerysetMixin, ListCreateAPIView):
    serializer_class = TaskListListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListRDApiView(TaskListUserQuerysetMixin, RetrieveDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = TaskListDetailSerializer


class TaskListTaskLCApiView(DynamicTaskListTaskQuerysetMixin, ListCreateAPIView):
    serializer_class = TaskDetailSerializer

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        add_task_to_tasklist(self.get_tasklist(), instance)


class TaskListTaskDestroyApiView(DynamicTaskListTaskQuerysetMixin, DestroyAPIView):
    def perform_destroy(self, instance):
        remove_task_from_tasklist(self.get_tasklist(), instance)

