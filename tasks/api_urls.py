from django.urls import path
from .api_views import TaskListListCreateApiView, TaskListRetrieveDestroyApiView


urlpatterns = [
    path('tasklists/', TaskListListCreateApiView.as_view(), name='api-tasklist-list'),
    path('tasklists/<slug:slug>/detail/', TaskListRetrieveDestroyApiView.as_view(), name='api-tasklist-detail')
]
