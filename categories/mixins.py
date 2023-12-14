from django.shortcuts import get_object_or_404


class UserCategoryQuerysetMixin:

    def get_queryset(self):
        return self.request.user.categories.all()


class DynamicCategoryTaskMixin:

    def get_category(self):
        user_categories = self.request.user.categories.all()
        category = get_object_or_404(user_categories, slug=self.kwargs.get('category', None))
        return category

    def get_queryset(self):
        return self.get_category().tasks.all()
