from django.contrib import admin
from .models import Task, TaskList, ListTaskPriority
# Register your models here.


@admin.display(description='Title')
def short_title(task: Task):
    return task.get_short_title()


class TaskAdmin(admin.ModelAdmin):
    list_display = [short_title, 'due_date', 'is_done']


class TaskListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title', ]}


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskList, TaskListAdmin)
admin.site.register(ListTaskPriority)
