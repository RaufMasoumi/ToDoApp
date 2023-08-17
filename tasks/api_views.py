from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Task
from .serializers import TaskDetailSerializer
from .views import UserTaskQuerysetMixin


class TaskRUDApiView(UserTaskQuerysetMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer


class TaskCreateApiView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
