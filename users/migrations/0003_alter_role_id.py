# Generated by Django 4.0.6 on 2022-07-09 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_role_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='id',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Admin'), (1, 'Instructor'), (2, 'Student')], primary_key=True, serialize=False),
        ),
    ]
