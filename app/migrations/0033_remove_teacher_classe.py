# Generated by Django 2.1 on 2018-10-17 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_remove_classes_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='classe',
        ),
    ]
