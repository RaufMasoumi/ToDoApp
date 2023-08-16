from django.urls import path
from .views import TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView


urlpatterns = [
    path('<uuid:pk>/detail/', TaskDetailView.as_view(), name='task-detail'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<uuid:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<uuid:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
]
