# Generated by Django 2.1.7 on 2019-06-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telaPrincipal', '0009_auto_20190609_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarefasgerais',
            name='sigla',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
