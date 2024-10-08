# Generated by Django 4.2.4 on 2023-08-16 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0007_remove_tasklist_tasks_remove_tasklist_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tasks', models.ManyToManyField(blank=True, related_name='tasklists', to='tasks.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasklists', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskListTaskPriority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_tasks', to='tasklists.tasklist')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
            ],
            options={
                'verbose_name_plural': 'List Task Priorities',
                'ordering': ['-number'],
                'default_related_name': 'priorities',
            },
        ),
    ]
