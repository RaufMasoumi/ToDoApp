from django.urls import path
from .api_views import TaskListLCApiView, TaskListRDApiView


urlpatterns = [
    path('', TaskListLCApiView.as_view(), name='api-tasklist-list'),
    path('<slug:slug>/detail/', TaskListRDApiView.as_view(), name='api-tasklist-detail')
]
