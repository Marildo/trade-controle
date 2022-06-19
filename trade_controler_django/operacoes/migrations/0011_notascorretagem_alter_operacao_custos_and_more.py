# Generated by Django 4.0.3 on 2022-06-07 10:49

import datetime
from django.db import migrations, models
import utils.enums


class Migration(migrations.Migration):

    dependencies = [
        ('operacoes', '0010_alter_operacao_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotasCorretagem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comprovante', models.IntegerField(default=0)),
                ('data_refrencia', models.DateTimeField(default=None, null=True)),
                ('tipo', models.IntegerField(choices=[(1, 'ACOES'), (2, 'FUTURO')], default=utils.enums.TipoNota['ACOES'])),
                ('data_upload', models.DateTimeField(default=datetime.datetime.now, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='operacao',
            name='custos',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='operacao',
            name='irpf',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='operacao',
            name='quantidade',
            field=models.FloatField(default=0),
        ),
    ]
