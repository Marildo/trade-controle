# Generated by Django 4.0.3 on 2022-03-26 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacoes', '0003_alter_operacao_data_compra_alter_operacao_data_venda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operacao',
            name='data_venda',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
