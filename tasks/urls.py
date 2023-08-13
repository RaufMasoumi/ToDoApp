from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from .views import TaskListListView, TaskListDetailView, TaskListCreateView, TaskListDeleteView


urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('tasklist-list')), name='home'),
    path('tasklists/', TaskListListView.as_view(), name='tasklist-list'),
    path('tasklists/<slug:slug>/detail/', TaskListDetailView.as_view(), name='tasklist-detail'),
    path('tasklists/create/', TaskListCreateView.as_view(), name='tasklist-create'),
    path('tasklists/<slug:slug>/delete/', TaskListDeleteView.as_view(), name='tasklist-delete')
]
