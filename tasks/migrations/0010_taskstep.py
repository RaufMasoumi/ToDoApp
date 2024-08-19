# Generated by Django 5.0.3 on 2024-08-19 08:32

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_task_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskStep',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=300)),
                ('number', models.IntegerField(blank=True, unique=True)),
                ('is_done', models.BooleanField(default=False)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='tasks.task')),
            ],
        ),
    ]
