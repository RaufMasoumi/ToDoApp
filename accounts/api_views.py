from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView
from .views import UserRedirectToPrimaryUrlMixin
from .serializers import CustomUserDetailSerializer
from .permissions import IsUserItSelfOrAdmin


class UserRedirectToPrimaryApiUrlMixin(UserRedirectToPrimaryUrlMixin):
    def get_redirect_url(self):
        return self.request.user.get_absolute_api_url()


class UserProfileRetrieveApiView(UserRedirectToPrimaryApiUrlMixin, RetrieveAPIView):
    queryset = get_user_model()
    serializer_class = CustomUserDetailSerializer
    lookup_field = 'slug'
    permission_classes = (IsUserItSelfOrAdmin, )
