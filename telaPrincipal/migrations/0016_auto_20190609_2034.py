# Generated by Django 2.1.7 on 2019-06-09 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telaPrincipal', '0015_auto_20190609_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hsmtarefasgerais',
            name='id_hsmemprocesso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='telaPrincipal.HSMEmProcesso'),
        ),
    ]
