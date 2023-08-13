from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView
from .serializers import CustomUserDetailSerializer


class UserProfileRetrieveApiView(RetrieveAPIView):
    queryset = get_user_model()
    serializer_class = CustomUserDetailSerializer
    lookup_field = 'slug'

    def get_object(self):
        if not self.kwargs.get('slug'):
            return self.request.user
        return super().get_object()
