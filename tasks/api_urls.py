from django.urls import path
from .api_views import TaskLCApiView, TaskRUDApiView


urlpatterns = [
    path('', TaskLCApiView.as_view(), name='api-task-list'),
    path('<uuid:pk>/', TaskRUDApiView.as_view(), name='api-task-detail'),
]
