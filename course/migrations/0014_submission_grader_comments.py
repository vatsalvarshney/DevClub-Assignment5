# Generated by Django 4.0.6 on 2022-08-06 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_submission_submitted_file_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='grader_comments',
            field=models.TextField(blank=True),
        ),
    ]
