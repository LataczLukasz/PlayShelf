# Generated by Django 5.1.5 on 2025-01-20 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playshelfapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='registration_date',
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
