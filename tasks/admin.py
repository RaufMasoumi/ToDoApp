from django.contrib import admin
from .models import Task
# Register your models here.


@admin.display(description='Title')
def short_title(task: Task):
    return task.get_short_title()


class TaskAdmin(admin.ModelAdmin):
    list_display = [short_title, 'due_date', 'is_done', 'user']


admin.site.register(Task, TaskAdmin)

