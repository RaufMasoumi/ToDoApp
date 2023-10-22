from django.shortcuts import get_object_or_404


class UserTaskListQuerysetMixin:
    def __init__(self, request=None):
        self.request = request

    def get_queryset(self):
        return self.request.user.tasklists.all()


class DynamicTaskListTaskQuerysetMixin:
    request = None
    kwargs = None

    def get_tasklist(self):
        user_tasklists = self.request.user.tasklists.all()
        tasklist = get_object_or_404(user_tasklists, slug=self.kwargs.get('tasklist'))
        return tasklist

    def get_queryset(self):
        return self.get_tasklist().tasks.all()
