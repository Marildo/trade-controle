# Generated by Django 4.0.3 on 2022-06-04 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ativos', '0002_alter_ativo_tipo'),
        ('operacoes', '0009_operacao_comprovante'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='operacao',
            unique_together={('ativo', 'pm_compra', 'data_encerramento', 'comprovante')},
        ),
    ]
