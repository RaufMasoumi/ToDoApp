# Generated by Django 4.2.4 on 2023-08-16 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_tasklist_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasklist',
            name='tasks',
        ),
        migrations.RemoveField(
            model_name='tasklist',
            name='user',
        ),
        migrations.DeleteModel(
            name='ListTaskPriority',
        ),
        migrations.DeleteModel(
            name='TaskList',
        ),
    ]
