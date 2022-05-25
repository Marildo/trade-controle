from decimal import Decimal
from typing import List

from django.db import models

from ativos.models import Ativo
from carteiras.models import Carteira


class Operacao(models.Model):
    class Meta:
        db_table = 'operacoes'

    id = models.AutoField(primary_key=True)
    data_compra = models.DateTimeField(null=True, default=None)
    data_venda = models.DateTimeField(null=True, default=None, blank=True)
    pm_compra = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    pm_venda = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    quantidade = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    custos = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    irpf = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    daytrade = models.BooleanField(default=False)
    encerrada = models.BooleanField(default=False)
    carteira = models.ForeignKey(Carteira, on_delete=models.DO_NOTHING)
    ativo = models.ForeignKey(Ativo, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.ativo.codigo

    @property
    def total(self) -> Decimal:
        return round(self.ativo.cotacao * self.quantidade, 2)

    @property
    def resultado(self) -> Decimal:
        return round((self.ativo.cotacao * self.quantidade) - (self.pm_compra * self.quantidade), 2)

    @property
    def resultado_percentual(self) -> Decimal:
        return round(self.ativo.cotacao / self.pm_compra * 100 - 100, 2)

    @classmethod
    def filter_by_carteira(cls, carteira_id: int) -> List:
        data = cls.objects.all().filter(carteira_id=carteira_id, encerrada=False)
        return list(data)
