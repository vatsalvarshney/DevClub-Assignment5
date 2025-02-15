# Generated by Django 4.0.6 on 2022-08-06 10:21

import course.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_remove_assignment_release_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='submitted_file',
            field=models.FileField(blank=True, null=True, upload_to=course.models.Submission.submission_upload),
        ),
        migrations.AddField(
            model_name='submission',
            name='submitted_file_icon',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='submission',
            name='submitting_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='grading_time',
            field=models.DateTimeField(),
        ),
    ]
