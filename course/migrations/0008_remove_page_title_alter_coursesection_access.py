# Generated by Django 4.0.6 on 2022-07-20 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_coursesection_show_on_main_page_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='title',
        ),
        migrations.AlterField(
            model_name='coursesection',
            name='access',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Author Only'), (2, 'Teachers Only'), (3, 'Everyone')], default=2),
        ),
    ]
