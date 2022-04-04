from django.db import models


class Carteira(models.Model):
    class Meta:
        db_table = 'carteiras'

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    saldo_ativos = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    saldo_caixa = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    @property
    def resultado_anual(self):
        rs = self.historico_anual.order_by('-ano')[:2]
        return rs[0].total - rs[1].total if len(rs) > 1 else rs[0].total

    @property
    def resultado_mensal(self):
        rs = self.historico_mensal.order_by('-mes')[:2]
        return rs[0].total - rs[1].total if len(rs) > 1 else rs[0].total

    @property
    def resultado_semanal(self):
        rs = self.historico_semanal.order_by('-semana')[:2]
        return rs[0].total - rs[1].total if len(rs) > 1 else rs[0].total

    def __str__(self) -> str:
        return str(self.nome)

    @classmethod
    def find_by_name(cls, nome: str):
        return cls.objects.filter(nome__iexact=nome).first()


class HistoricoAnual(models.Model):
    class Meta:
        db_table = 'historico_anual'

    id = models.AutoField(primary_key=True)
    total = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    ano = models.DateField(null=False)
    carteira = models.ForeignKey(Carteira, on_delete=models.CASCADE, related_name='historico_anual')


class HistoricoMensal(models.Model):
    class Meta:
        db_table = 'historico_mensal'

    id = models.AutoField(primary_key=True)
    total = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    mes = models.DateField(null=False)
    carteira = models.ForeignKey(Carteira, on_delete=models.CASCADE, related_name='historico_mensal')

    def __str__(self):
        return f'{self.mes} - {self.total}'


class HistoricoSemanal(models.Model):
    class Meta:
        db_table = 'historico_semanal'

    id = models.AutoField(primary_key=True)
    total = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    semana = models.DateField(null=False)
    carteira = models.ForeignKey(Carteira, on_delete=models.CASCADE, related_name='historico_semanal')
