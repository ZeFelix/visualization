# Generated by Django 2.1 on 2018-09-07 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_node_node_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='node_end',
            field=models.BooleanField(default=False, verbose_name='Nó fim?'),
        ),
    ]