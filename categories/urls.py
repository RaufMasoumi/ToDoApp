from django.urls import path
from .views import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<slug:slug>/detail/', CategoryDetailView.as_view(), name='category-detail'),
    path('create/', CategoryCreateView.as_view(), name='category-create'),
    path('<slug:slug>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('<slug:slug>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
]
