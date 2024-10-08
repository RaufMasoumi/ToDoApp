"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # Local
    path('', RedirectView.as_view(pattern_name='tasklist-list'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
    path('tasklists/', include('tasklists.urls')),
    path('categories/', include('categories.urls')),
]

api_urlpatterns = [
    path('api/accounts/', include('rest_framework.urls')),
    path('api/accounts/rest-auth/', include('dj_rest_auth.urls')),
    # Local
    path('api/', RedirectView.as_view(pattern_name='api-tasklist-list'), name='api-home'),
    path('api/accounts/', include('accounts.api_urls')),
    path('api/tasks/', include('tasks.api_urls')),
    path('api/tasklists/', include('tasklists.api_urls')),
    path('api/categories/', include('categories.api_urls'))

]

urlpatterns += api_urlpatterns
