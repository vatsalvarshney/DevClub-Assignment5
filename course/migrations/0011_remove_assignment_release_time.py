# Generated by Django 4.0.6 on 2022-08-03 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_alter_assignment_late_due_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='release_time',
        ),
    ]
