# Generated by Django 4.0.3 on 2022-03-23 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carteiras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carteira',
            name='resultado_anual',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='carteira',
            name='resultado_diario',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='carteira',
            name='resultado_mensal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='carteira',
            name='resultado_semanal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='carteira',
            name='resultado_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='carteira',
            name='saldo_ativos',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='carteira',
            name='saldo_caixa',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
