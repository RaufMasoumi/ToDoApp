from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# Create your models here.
DEFAULT_TASKLISTS = {
    'all': 'All Tasks',
    'important': 'Important Tasks',
    'daily': 'Daily Tasks',
    'done': 'Completed Tasks',
}


class Task(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(get_user_model(), related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    due_date = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False, blank=True)
    is_daily = models.BooleanField(default=False, blank=True)
    is_important = models.BooleanField(default=False, blank=True)
    is_not_important = models.BooleanField(default=False, blank=True)
    is_timely_important = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    done_at = models.DateTimeField(blank=True, null=True)
    __is_done = None

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__is_done = self.is_done

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

    def get_absolute_update_url(self):
        return reverse('task-update', kwargs={'pk': self.pk})

    def get_absolute_delete_url(self):
        return reverse('task-delete', kwargs={'pk': self.pk})

    def get_short_title(self):
        if len(self.title) >= 30:
            short_title = self.title[:30] + ' ...'
        else:
            short_title = self.title
        return short_title

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.__is_done != self.is_done:
            if self.is_done:
                self.done_at = timezone.now()
            else:
                self.done_at = None
            self.__is_done = self.is_done
        elif self.__is_done == self.is_done and self.__is_done:
            if not self.done_at:
                self.done_at = timezone.now()

        return super().save(force_insert, force_update, using, update_fields)


@receiver(post_save, sender=Task)
def add_task_to_default_tasklist(instance, created, **kwargs):
    task = instance
    statuses = list(DEFAULT_TASKLISTS.keys())
    statuses.pop(statuses.index('all'))
    if created:
        task.user.tasklists.all_tasks().tasks.add(task)
    for status in statuses:
        bound_func = getattr(task.user.tasklists, status, None)
        if callable(bound_func):
            default_tasklist = bound_func()
            is_status = getattr(task, f'is_{status}', False)
            if default_tasklist:
                if is_status and task not in default_tasklist.tasks.all():
                    default_tasklist.tasks.add(task)
                elif not is_status and task in default_tasklist.tasks.all():
                    default_tasklist.tasks.remove(task)
