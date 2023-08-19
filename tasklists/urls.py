from django.urls import path
from .views import TaskListListView, TaskListDetailView, TaskListCreateView, TaskListUpdateView, TaskListDeleteView, \
    TaskListTaskCreateView, TaskListTaskUpdateView, TaskListTaskDeleteView

urlpatterns = [
    path('', TaskListListView.as_view(), name='tasklist-list'),
    path('<slug:slug>/detail/', TaskListDetailView.as_view(), name='tasklist-detail'),
    path('create/', TaskListCreateView.as_view(), name='tasklist-create'),
    path('<slug:slug>/update/', TaskListUpdateView.as_view(), name='tasklist-update'),
    path('<slug:slug>/delete/', TaskListDeleteView.as_view(), name='tasklist-delete'),
    path('<slug:tasklist>/tasks/create/', TaskListTaskCreateView.as_view(), name='tasklist-task-create'),
    path('<slug:tasklist>/tasks/<uuid:pk>/update/', TaskListTaskUpdateView.as_view(), name='tasklist-task-update'),
    path('<slug:tasklist>/tasks/<uuid:pk>/delete/', TaskListTaskDeleteView.as_view(), name='tasklist-task-delete'),
]
