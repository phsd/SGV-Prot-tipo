# Generated by Django 2.1.7 on 2019-06-09 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telaPrincipal', '0013_hsmemprocesso_id_tarefasgerais'),
    ]

    operations = [
        migrations.AddField(
            model_name='hsmtarefasgerais',
            name='diaeHoraFim',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hsmtarefasgerais',
            name='diaeHoraInicio',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
