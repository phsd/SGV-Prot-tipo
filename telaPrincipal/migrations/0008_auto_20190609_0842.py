# Generated by Django 2.1.7 on 2019-06-09 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telaPrincipal', '0007_auto_20190524_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='hourlyschedulemanagementrealizado',
            name='id_usuario',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hsmemprocesso',
            name='id_usuario',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]