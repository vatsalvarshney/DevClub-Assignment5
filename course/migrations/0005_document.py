# Generated by Django 4.0.6 on 2022-07-14 14:37

import course.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0004_coursesection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=500, upload_to=course.models.materialUpload)),
                ('date_posted', models.DateTimeField()),
                ('access', models.PositiveIntegerField(choices=[(1, 'Author Only'), (2, 'Teachers Only'), (3, 'Everyone')], default=1)),
                ('filename', models.CharField(default=None, max_length=256)),
                ('author', models.ForeignKey(limit_choices_to={'role': 2}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.coursesection')),
            ],
        ),
    ]
