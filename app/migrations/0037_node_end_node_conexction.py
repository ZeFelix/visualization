# Generated by Django 2.1 on 2018-10-19 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_node_is_way'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='end_node_conexction',
            field=models.BooleanField(default=False, verbose_name='Nó que conecta todos os nós folhas (FIM)'),
        ),
    ]
