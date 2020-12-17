# Generated by Django 3.1.3 on 2020-12-11 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0007_auto_20201210_2353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studenttest',
            name='quiz',
        ),
        migrations.AddField(
            model_name='studenttest',
            name='quiz',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz'),
        ),
        migrations.RemoveField(
            model_name='studenttest',
            name='student',
        ),
        migrations.AddField(
            model_name='studenttest',
            name='student',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]