from django.urls import path
from .api_views import CategoryLCApiView, CategoryRUDApiView, CategoryTaskLCApiView, CategoryTaskDestroyApiView

urlpatterns = [
    path('', CategoryLCApiView.as_view(), name='api-category-list'),
    path('<slug:slug>/', CategoryRUDApiView.as_view(), name='api-category-detail'),
    path('<slug:category>/tasks/', CategoryTaskLCApiView.as_view(), name='api-category-task-list'),
    path('<slug:category>/tasks/<uuid:pk>/delete/', CategoryTaskDestroyApiView.as_view(), name='api-category-task-delete'),
]
