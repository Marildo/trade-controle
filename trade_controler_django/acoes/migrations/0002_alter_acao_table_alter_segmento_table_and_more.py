# Generated by Django 4.0.3 on 2022-03-12 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acoes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='acao',
            table='acoes',
        ),
        migrations.AlterModelTable(
            name='segmento',
            table='segmentos',
        ),
        migrations.AlterModelTable(
            name='setor',
            table='setores',
        ),
        migrations.AlterModelTable(
            name='subsetor',
            table='subsetores',
        ),
    ]