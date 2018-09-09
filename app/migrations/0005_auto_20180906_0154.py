# Generated by Django 2.1 on 2018-09-06 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20180906_0144'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome do Curso')),
                ('node_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Node', verbose_name='Nó raiz')),
            ],
        ),
        migrations.RemoveField(
            model_name='classes',
            name='node',
        ),
        migrations.AddField(
            model_name='classes',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Course', verbose_name='Curso'),
        ),
    ]