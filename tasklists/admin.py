from django.contrib import admin
from .models import TaskList, TaskListTaskPriority
# Register your models here.


class TaskListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title', ]}


admin.site.register(TaskList, TaskListAdmin)
admin.site.register(TaskListTaskPriority)
