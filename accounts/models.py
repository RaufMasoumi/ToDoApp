from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
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
