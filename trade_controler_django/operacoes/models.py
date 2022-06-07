from decimal import Decimal
from typing import List
from datetime import datetime

from django.db import models

from ativos.models import Ativo
from carteiras.models import Carteira


class Operacao(models.Model):
    class Meta:
        db_table = 'operacoes'
        unique_together = (('ativo', 'pm_compra', 'data_encerramento', 'comprovante'),)

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
    comprovante = models.IntegerField(default=0)
    data_encerramento = models.DateField(default=datetime.now)
    carteira = models.ForeignKey(Carteira, on_delete=models.DO_NOTHING)
    ativo = models.ForeignKey(Ativo, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.ativo.codigo

    @property
    def total(self) -> Decimal:
        return 0 if self.encerrada else round(self.ativo.cotacao * self.quantidade, 2)

    @property
    def resultado(self) -> Decimal:
        if self.encerrada:
            return round(Decimal((self.pm_venda - self.pm_compra) + self.custos + self.irpf) * self.quantidade, 2)
        else:
            return Decimal(round((self.ativo.cotacao * self.quantidade) - (self.pm_compra * self.quantidade), 2))

    @property
    def resultado_percentual(self) -> Decimal:
        if self.encerrada:
            return round((self.pm_venda * self.quantidade) / (
                    (self.pm_compra * self.quantidade) + (self.custos + self.irpf)) * 100 - 100, 2)
        else:
            return round(self.ativo.cotacao / self.pm_compra * 100 - 100, 2)

    @classmethod
    def filter_by_carteira(cls, carteira_id: int) -> List:
        query = cls.objects.filter(carteira_id=carteira_id, encerrada=False)
        data = list(query)

        first_day = datetime.today().replace(day=1)
        query = cls.objects.filter(carteira_id=carteira_id, data_encerramento__gte=first_day, encerrada=True)
        data += list(query)

        return data
