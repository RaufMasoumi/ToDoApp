from django.db import models
from django.utils import timezone
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.forms import ValidationError
# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    due_date = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False, blank=True)
    is_important = models.BooleanField(default=False, blank=True)
    is_not_important = models.BooleanField(default=False, blank=True)
    is_timely_important = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    done_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.title

    def get_short_title(self):
        if len(self.title) >= 30:
            short_title = self.title[:30] + ' ...'
        else:
            short_title = self.title
        return short_title

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.is_done:
            self.done_at = timezone.now()

        return super().save(force_insert, force_update, using, update_fields)


class TaskList(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='tasklists', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    tasks = models.ManyToManyField(Task, related_name='lists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasklist-detail', kwargs={'slug': self.slug})

    def clean_tasks(self):
        if self.tasks.exclude(user=self.user).exists():
            raise ValidationError('There should not be the tasks that are not for user in user\'s task list!',
                                  code='invalid')

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = self.title.lower()
        return super().save(force_insert, force_update, using, update_fields)


class ListTaskPriority(models.Model):
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


def update_task_number(task_p: ListTaskPriority, new_number: int):
    old_number = task_p.number
    task_p.number = new_number
    for i in range(old_number + 1, new_number + 1):
        p = ListTaskPriority.objects.get(number=i)
        p.number -= 1
        p.save()
    task_p.save()


@receiver(m2m_changed, sender=TaskList.tasks.through)
def create_priority_for_task(instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            task = Task.objects.get(pk=pk)
            new_number = ListTaskPriority.objects.count() + 1
            ListTaskPriority.objects.create(task=task, list=instance, number=new_number)
