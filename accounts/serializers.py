from django.contrib.auth import get_user_model
from rest_framework.serializers import HyperlinkedModelSerializer


class CustomUserDetailSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['url', 'username', 'first_name', 'last_name', 'date_joined', 'slug']
        extra_kwargs = {
            'url': {'view_name': 'api-user-detail', 'lookup_field': 'slug'},
        }
