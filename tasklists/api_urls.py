from django.urls import path
from .api_views import TaskListLCApiView, TaskListRDApiView, TaskListTaskLCApiView, TaskListTaskDestroyApiView


urlpatterns = [
    path('', TaskListLCApiView.as_view(), name='api-tasklist-list'),
    path('<slug:slug>/detail/', TaskListRDApiView.as_view(), name='api-tasklist-detail'),
    path('<slug:tasklist>/tasks/', TaskListTaskLCApiView.as_view(), name='api-tasklist-task-list'),
    path('<slug:tasklist>/tasks/<uuid:pk>/delete/', TaskListTaskDestroyApiView.as_view(), name='api-tasklist-task-delete'),
]
