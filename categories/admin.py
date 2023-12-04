from django.contrib import admin
from .models import Category
# Register your models here.


@admin.display(description='Count of Tasks')
def tasks_count(category: Category):
    return category.tasks.count()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', tasks_count]
    prepopulated_fields = {
        'slug': ['title', ]
    }


admin.site.register(Category, CategoryAdmin)
