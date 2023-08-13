from django.urls import path
from .api_views import UserProfileRetrieveApiView


urlpatterns = [
    path('profile/', UserProfileRetrieveApiView.as_view(), name='api-user-detail'),
    path('profile/<slug:slug>/', UserProfileRetrieveApiView.as_view(), name='api-user-detail'),
]