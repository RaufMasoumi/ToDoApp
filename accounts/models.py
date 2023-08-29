from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# Create your models here.


class CustomUser(AbstractUser):
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.username
        return super().save(*args, **kwargs)
