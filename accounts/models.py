from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.


class CustomUser(AbstractUser):
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'slug': self.slug})

    def get_absolute_api_url(self):
        return reverse('api-user-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)


@receiver(post_save, sender=CustomUser)
def create_token_for_user(instance, created, **kwargs):
    if created:
        Token.objects.create(
            user=instance
        )


from tasklists.models import TaskList
from tasks.models import DEFAULT_TASKLISTS


@receiver(post_save, sender=CustomUser)
def create_default_tasklists(instance, created, **kwargs):
    if created:
        default_tasklists = [
            TaskList(user=instance, title=title, slug=slugify(title), is_default=True) for title in DEFAULT_TASKLISTS.values()
        ]
        TaskList.objects.bulk_create(default_tasklists)
