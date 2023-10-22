from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.exceptions import MultipleObjectsReturned
from tasks.models import Task, DEFAULT_TASKLISTS
import uuid
# Create your models here.


class TaskListManager(models.Manager):

    def handle_multiple_exception(getter):
        def handler(self):
            try:
                tasklist = getter(self)
            except MultipleObjectsReturned:
                tasklist = None
            return tasklist
        return handler

    # warning: only use these methods from user tasklist manager
    @handle_multiple_exception
    def all_tasks(self):
        return self.get(title=DEFAULT_TASKLISTS['all_tasks'])

    @handle_multiple_exception
    def important(self):
        return self.get(title=DEFAULT_TASKLISTS['important'])

    @handle_multiple_exception
    def daily(self):
        return self.get(title=DEFAULT_TASKLISTS['daily'])

    @handle_multiple_exception
    def done(self):
        return self.get(title=DEFAULT_TASKLISTS['done'])

    def default_tasklists(self):
        return self.filter(is_default=True)

    def non_default_tasklists(self):
        return self.filter(is_default=False)


class TaskList(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(get_user_model(), related_name='tasklists', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    tasks = models.ManyToManyField(Task, related_name='tasklists', blank=True)
    is_default = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TaskListManager()

    class Meta:
        ordering = ['-created_at', 'title']
        permissions = [
            ('default_tasklist', 'Can change default task list')
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasklist-detail', kwargs={'slug': self.slug})

    def get_absolute_update_url(self):
        return reverse('tasklist-update', kwargs={'slug': self.slug})

    def get_absolute_delete_url(self):
        return reverse('tasklist-delete', kwargs={'slug': self.slug})

    def clean_title(self):
        if self.user.tasklists.filter(title=self.title).exists():
            raise ValidationError('TaskList title should be unique!', code='invalid')

    def clean_tasks(self):
        if self.tasks.exclude(user=self.user).exists():
            raise ValidationError('There should not be the tasks that are not for user in user\'s task list!',
                                  code='invalid')

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(force_insert, force_update, using, update_fields)


class TaskListTaskPriority(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='ordered_tasks')
    number = models.IntegerField()

    class Meta:
        ordering = ['-number']
        default_related_name = 'priorities'
        verbose_name_plural = 'List Task Priorities'

    def __str__(self):
        return f'\'{self.task.get_short_title()}\' priority in \'{self.list}\''
    #
    # def save(
    #     self, force_insert=False, force_update=False, using=None, update_fields=None
    # ):
    #     if not ListTaskPriority.objects.filter(pk=self.pk).exists():
    #         self.number = 1


def update_task_number(task_p: TaskListTaskPriority, new_number: int):
    old_number = task_p.number
    task_p.number = new_number
    for i in range(old_number + 1, new_number + 1):
        p = TaskListTaskPriority.objects.get(number=i)
        p.number -= 1
        p.save()
    task_p.save()


@receiver(m2m_changed, sender=TaskList.tasks.through)
def create_priority_for_task(instance, action, pk_set, **kwargs):
    if action == 'post_add':
        if isinstance(instance, Task):
            task = instance
            for pk in pk_set:
                if TaskList.objects.filter(pk=pk).exists():
                    tasklist = TaskList.objects.get(pk=pk)
                    new_number = tasklist.tasks.count()
                    TaskListTaskPriority.objects.create(task=task, list=tasklist, number=new_number)

        elif isinstance(instance, TaskList):
            tasklist = instance
            for pk in pk_set:
                if Task.objects.filter(pk=pk).exists():
                    task = Task.objects.get(pk=pk)
                    new_number = tasklist.tasks.count()
                    TaskListTaskPriority.objects.create(task=task, list=instance, number=new_number)
