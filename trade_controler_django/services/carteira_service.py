"""
Created on 27/03/2022
by MarildoCesar
"""
from datetime import date, timedelta
from typing import List

from carteiras.models import Carteira, HistoricoAnual, HistoricoMensal, HistoricoSemanal
from operacoes.models import Operacao


class CarteiraService:

    @staticmethod
    def summarize(carteira: Carteira, operacoes: List[Operacao]) -> Carteira:
        saldo_ativos = 0
        for item in operacoes:
            saldo_ativos += item.total

        carteira.saldo_ativos = saldo_ativos
        carteira.save()

        year = date.today().year
        month = date.today().month

        ano = date(year, 1, 1)
        hist_anual = HistoricoAnual.objects.filter(carteira=carteira, ano=ano).first()
        if not hist_anual:
            hist_anual = HistoricoAnual(carteira=carteira, total=saldo_ativos, ano=ano)

        hist_anual.total = saldo_ativos
        hist_anual.save()

        mes = date(year, month + 1, 1) - timedelta(days=1)
        hist_mensal = HistoricoMensal.objects.filter(carteira=carteira, mes=mes).first()
        if not hist_mensal:
            hist_mensal = HistoricoMensal(carteira=carteira, total=saldo_ativos, mes=mes)

        hist_mensal.total = saldo_ativos
        hist_mensal.save()

        semana = (date.today() - timedelta(days=date.today().isoweekday())) + timedelta(days=6)
        hist_semanal = HistoricoSemanal.objects.filter(carteira=carteira, semana=semana).first()
        if not hist_semanal:
            hist_semanal = HistoricoSemanal(carteira=carteira, total=saldo_ativos, semana=semana)

        hist_semanal.total = saldo_ativos
        hist_semanal.save()

        return carteira
