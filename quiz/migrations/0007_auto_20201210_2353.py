# Generated by Django 3.1.3 on 2020-12-10 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_studenttest_studenttestanswer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studenttest',
            old_name='test',
            new_name='quiz',
        ),
    ]