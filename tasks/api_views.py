from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework.backends import DjangoFilterBackend
from .serializers import TaskDetailSerializer
from .mixins import UserTaskQuerysetMixin
from .filters import TaskFilterSet


class TaskLCApiView(UserTaskQuerysetMixin, ListCreateAPIView):
    serializer_class = TaskDetailSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TaskFilterSet

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskRUDApiView(UserTaskQuerysetMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer


