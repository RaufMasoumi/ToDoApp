

class UserCategoryQuerysetMixin:
    request = None

    def get_queryset(self):
        return self.request.user.categories.all()
