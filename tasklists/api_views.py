from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from .serializers import TaskListListSerializer, TaskListDetailSerializer
from .views import TaskListUserQuerysetMixin


class TaskListLCApiView(TaskListUserQuerysetMixin, ListCreateAPIView):
    serializer_class = TaskListListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListRDApiView(TaskListUserQuerysetMixin, RetrieveDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = TaskListDetailSerializer
