# Generated by Django 4.2.4 on 2023-09-06 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasklists', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tasklist',
            options={'ordering': ['-created_at', 'title']},
        ),
    ]
