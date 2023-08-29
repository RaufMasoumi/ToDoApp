from django.urls import path
from .views import UserProfile


urlpatterns = [
    path('profile/', UserProfile.as_view(), name='user-detail'),
    path('profile/<slug:slug>/', UserProfile.as_view(), name='user-detail'),
]
