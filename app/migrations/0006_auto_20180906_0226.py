# Generated by Django 2.1 on 2018-09-06 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180906_0154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='node_children',
        ),
        migrations.AddField(
            model_name='node',
            name='node_children',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Node', verbose_name='Nó Filho'),
        ),
    ]