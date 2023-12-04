from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
import uuid
# Create your models here.


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='categories')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.title)
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})
