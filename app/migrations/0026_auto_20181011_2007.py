# Generated by Django 2.1 on 2018-10-11 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_teacher'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': 'Professor', 'verbose_name_plural': 'Professores'},
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='classe',
        ),
        migrations.AddField(
            model_name='teacher',
            name='classe',
            field=models.ManyToManyField(to='app.Classes'),
        ),
    ]