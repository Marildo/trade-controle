from django.db import models

from ativos.models import Ativo
from carteiras.models import Carteira


class Operacao(models.Model):
    class Meta:
        db_table = 'operacoes'

    id = models.AutoField(primary_key=True)
    data_compra = models.DateTimeField(null=True, default=None)
    data_venda = models.DateTimeField(null=True, default=None, blank=True)
    pm_compra = models.FloatField(default=0)
    pm_venda = models.FloatField(default=0)
    quantidade = models.FloatField(default=0)
    custos = models.FloatField(default=0)
    daytrade = models.BooleanField(default=False)
    encerrada = models.BooleanField(default=False)
    carteira = models.ForeignKey(Carteira, on_delete=models.DO_NOTHING)
    ativo = models.ForeignKey(Ativo, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.ativo.codigo