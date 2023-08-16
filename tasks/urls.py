from django.urls import path
from .views import TaskUpdateView


urlpatterns = [
    path('<uuid:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
]
