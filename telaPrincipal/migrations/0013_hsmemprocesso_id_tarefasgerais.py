# Generated by Django 2.1.7 on 2019-06-09 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telaPrincipal', '0012_remove_hsmemprocesso_id_tarefasgerais'),
    ]

    operations = [
        migrations.AddField(
            model_name='hsmemprocesso',
            name='id_tarefasgerais',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='telaPrincipal.TarefasGerais'),
        ),
    ]
