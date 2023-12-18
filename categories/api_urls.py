from django.urls import path
from .api_views import CategoryLCApiView, CategoryRUDApiView

urlpatterns = [
    path('', CategoryLCApiView.as_view(), name='api-category-list'),
    path('<slug:slug>/', CategoryRUDApiView.as_view(), name='api-category-detail')
]
