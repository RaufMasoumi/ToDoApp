# Generated by Django 5.0.3 on 2024-08-19 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_taskstep'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskstep',
            name='number',
        ),
    ]
