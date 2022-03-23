from django.db import models


class Carteira(models.Model):
    class Meta:
        db_table = 'carteiras'

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    saldo_ativos = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    saldo_caixa = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    resultado_diario = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    resultado_semanal = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    resultado_mensal = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    resultado_anual = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    resultado_total = models.DecimalField(decimal_places=2, max_digits=10, default=0)


    def __str__(self) -> str:
        return self.nome
