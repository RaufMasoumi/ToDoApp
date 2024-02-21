from django.contrib import admin
from .models import TaskList
# Register your models here.


class TaskListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title', ]}
    list_display = ['title', 'user']


admin.site.register(TaskList, TaskListAdmin)
