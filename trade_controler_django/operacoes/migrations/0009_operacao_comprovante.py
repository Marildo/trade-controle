# Generated by Django 4.0.3 on 2022-06-04 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacoes', '0008_operacao_data_encerramento'),
    ]

    operations = [
        migrations.AddField(
            model_name='operacao',
            name='comprovante',
            field=models.IntegerField(default=0),
        ),
    ]