# Generated by Django 2.1 on 2018-10-17 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20181016_0057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='percentage_completed',
        ),
        migrations.AddField(
            model_name='studentinformations',
            name='amount_access',
            field=models.IntegerField(default=0, verbose_name='quantidade de acesso'),
        ),
        migrations.AddField(
            model_name='studentinformations',
            name='percentage_completed',
            field=models.IntegerField(default=0, verbose_name='Porcentagem concluida'),
        ),
    ]
