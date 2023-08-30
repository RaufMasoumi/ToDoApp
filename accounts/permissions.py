from rest_framework.permissions import BasePermission, SAFE_METHODS


def is_safe_request(request):
    return request.method in SAFE_METHODS


class IsUserItSelfOrAdmin(BasePermission):
    """
        Checks if the user is authenticated and the user is the requested object or the user is admin.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif obj == request.user:
            return True
        else:
            return False
