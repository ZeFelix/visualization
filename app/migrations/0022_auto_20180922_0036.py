# Generated by Django 2.1 on 2018-09-22 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_studentinformations_is_evaluated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentinformations',
            name='is_evaluated',
        ),
        migrations.AddField(
            model_name='node',
            name='is_evaluated',
            field=models.BooleanField(default=True, verbose_name='Esse nó é avaliado?'),
        ),
    ]