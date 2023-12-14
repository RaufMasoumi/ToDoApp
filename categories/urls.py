from django.urls import path
from .views import (CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
                    CategoryTaskCreateView, CategoryTaskUpdateView, CategoryTaskDeleteView)

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<slug:slug>/detail/', CategoryDetailView.as_view(), name='category-detail'),
    path('create/', CategoryCreateView.as_view(), name='category-create'),
    path('<slug:slug>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('<slug:slug>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('<slug:category>/tasks/create/', CategoryTaskCreateView.as_view(), name='category-task-create'),
    path('<slug:category>/tasks/<uuid:pk>/update/', CategoryTaskUpdateView.as_view(), name='category-task-update'),
    path('<slug:category>/tasks/<uuid:pk>/delete/', CategoryTaskDeleteView.as_view(), name='category-task-delete'),
]
