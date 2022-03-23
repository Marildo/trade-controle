from django.db import models

from ativos.models import Ativo
from carteiras.models import Carteira


class Operacao(models.Model):
    class Meta:
        db_table = 'operacoes'

    id = models.AutoField(primary_key=True)
    data_compra = models.DateTimeField()
    data_venda = models.DateTimeField()
    pm_compra = models.FloatField(default=0)
    pm_venda = models.FloatField(default=0)
    quantidade = models.FloatField(default=0)
    custos = models.FloatField(default=0)
    carteira = models.ForeignKey(Carteira, on_delete=models.DO_NOTHING)
    ativo = models.ForeignKey(Ativo, on_delete=models.DO_NOTHING)

    