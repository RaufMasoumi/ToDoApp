from django.urls import path
from .api_views import TaskRUDApiView, TaskCreateApiView


urlpatterns = [
    path('<uuid:pk>/', TaskRUDApiView.as_view(), name='api-task-detail'),
    path('create/', TaskCreateApiView.as_view(), name='api-task-create'),
]
