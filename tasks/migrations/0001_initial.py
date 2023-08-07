# Generated by Django 4.2.3 on 2023-08-02 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('is_done', models.BooleanField(blank=True, default=False)),
                ('is_important', models.BooleanField(blank=True, default=False)),
                ('is_not_important', models.BooleanField(blank=True, default=False)),
                ('is_timely_important', models.BooleanField(blank=True, default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('done_at', models.DateTimeField()),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tasks', models.ManyToManyField(related_name='lists', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='ListTaskPriority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_tasks', to='tasks.tasklist')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
            ],
            options={
                'verbose_name_plural': 'List Task Priorities',
                'ordering': ['-number'],
                'default_related_name': 'priorities',
            },
        ),
    ]