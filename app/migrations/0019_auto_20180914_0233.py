# Generated by Django 2.1 on 2018-09-14 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20180914_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinformations',
            name='notes',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Nota do Aluno'),
        ),
    ]
