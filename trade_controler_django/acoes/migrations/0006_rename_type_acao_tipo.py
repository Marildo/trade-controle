# Generated by Django 4.0.3 on 2022-03-16 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acoes', '0005_acao_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acao',
            old_name='type',
            new_name='tipo',
        ),
    ]