from django.urls import path
from .views import TaskListListView, TaskListDetailView, TaskListCreateView


urlpatterns = [
    path('', TaskListListView.as_view(), name='tasklist-list'),
    path('<slug:slug>/detail/', TaskListDetailView.as_view(), name='tasklist-detail'),
    path('create/', TaskListCreateView.as_view(), name='tasklist-create'),
]
