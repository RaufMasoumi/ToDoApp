from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid

# Create your models here.
DEFAULT_TASKLISTS = {
    'all_tasks': 'All Tasks',
    'important': 'Important Tasks',
    'daily': 'Daily Tasks',
    'done': 'Completed Tasks',
}
DEFAULT_TASK_STATUSES = {getter: f'is_{getter}' for getter in DEFAULT_TASKLISTS.keys() if getter != 'all_tasks'}


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
    __is_daily = None
    __is_important = None

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__is_done = self.is_done
        self.__is_daily = self.is_daily
        self.__is_important = self.is_important

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

        # checking if the object is created
        if self._state.adding:
            add_task_to_tasklist(self.user.tasklists.all_tasks(), self)
        for getter, is_status in DEFAULT_TASK_STATUSES.items():
            status = getattr(self, is_status, None)
            private_is_status = f'_Task__{is_status}'
            private_status = getattr(self, private_is_status, None)
            bound_func = getattr(self.user.tasklists, getter)
            if callable(bound_func):
                default_tasklist = bound_func()
                if private_status != status:
                    if status:
                        add_task_to_tasklist(default_tasklist, self)
                        if is_status == 'is_done':
                            self.done_at = timezone.now()
                    else:
                        remove_task_from_tasklist(default_tasklist, self)
                        if is_status == 'is_done':
                            self.done_at = None
                    setattr(self, private_is_status, status)

                # if when creating, status has been set true
                elif private_status == status and private_is_status:
                    add_task_to_tasklist(default_tasklist, self)
                    if is_status == 'is_done' and self not in default_tasklist.tasks.all():
                        self.done_at = timezone.now()

        return super().save(force_insert, force_update, using, update_fields)


def add_task_to_tasklist(tasklist, task):
    if task not in tasklist.tasks.all():
        tasklist.tasks.add(task)
        tasklist.save()
    return tasklist


def remove_task_from_tasklist(tasklist, task):
    if task in tasklist.tasks.all():
        tasklist.tasks.remove(task)
        tasklist.save()
    return tasklist
