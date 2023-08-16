from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
# Create your models here.


class TaskManager(models.Manager):
    def user_task(self, user):
        return self.filter(user=user)


class Task(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
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
    objects = TaskManager()

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

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
