# Generated by Django 4.2.3 on 2023-08-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
