from django.urls import path
from .views import (TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
                    TaskStepCreateView, TaskStepUpdateView, TaskStepDeleteView)


urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('<uuid:pk>/detail/', TaskDetailView.as_view(), name='task-detail'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<uuid:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<uuid:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasksteps/create/', TaskStepCreateView.as_view(), name='taskstep-create'),
    path('tasksteps/<uuid:pk>/update/', TaskStepUpdateView.as_view(), name='taskstep-update'),
    path('tasksteps/<uuid:pk>/delete/', TaskStepDeleteView.as_view(), name='taskstep-delete'),
]
