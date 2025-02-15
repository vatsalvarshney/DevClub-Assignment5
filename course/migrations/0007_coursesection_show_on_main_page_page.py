# Generated by Django 4.0.6 on 2022-07-20 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursesection',
            name='show_on_main_page',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='course.item')),
                ('section', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='course.coursesection')),
            ],
        ),
    ]
