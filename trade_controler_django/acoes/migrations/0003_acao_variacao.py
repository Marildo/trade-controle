# Generated by Django 4.0.3 on 2022-03-13 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acoes', '0002_alter_acao_table_alter_segmento_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='acao',
            name='variacao',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
