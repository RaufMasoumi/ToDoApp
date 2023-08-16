from django.urls import path
from .api_views import TaskListListCreateApiView, TaskListRetrieveDestroyApiView


urlpatterns = [
    path('', TaskListListCreateApiView.as_view(), name='api-tasklist-list'),
    path('<slug:slug>/detail/', TaskListRetrieveDestroyApiView.as_view(), name='api-tasklist-detail')
]
