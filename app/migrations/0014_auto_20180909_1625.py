# Generated by Django 2.1 on 2018-09-09 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20180909_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='depth',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Level', verbose_name='Nível'),
        ),
    ]
