from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import TaskDetailSerializer
from .mixins import UserTaskQuerysetMixin


class TaskLCApiView(UserTaskQuerysetMixin, ListCreateAPIView):
    serializer_class = TaskDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskRUDApiView(UserTaskQuerysetMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer


