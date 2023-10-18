from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.permissions import BasePermission, SAFE_METHODS


class DefaultTaskListPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif obj.is_default and not request.user.has_perm('tasklists.default_tasklist'):
            return False
        return True


class TaskDefaultTaskListPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif view.get_tasklist().is_default and not request.user.has_perm('tasklists.default_tasklist'):
            return False
        return True


class DefaultTaskListPermissionMixin(PermissionRequiredMixin):
    tasklist_getter = 'get_object'

    def get_permission_required(self):
        tasklist = self.get_object() if self.tasklist_getter == 'get_object' else self.get_tasklist()
        if tasklist and tasklist.is_default:
            return ['tasklists.default_tasklist', ]

