from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from operacoes.models import Operacao
from services.carteira_service import CarteiraService
from .models import Carteira


def index(request: WSGIRequest):
    carteiras = Carteira.objects.all()

    ativos = 0
    ano = 0
    mes = 0
    semana = 0
    for i in carteiras:
        ativos += i.saldo_ativos
        ano += i.resultado_anual
        mes += i.resultado_mensal
        semana += i.resultado_semanal

    totais = {
        'ativos': ativos,
        'ano': ano,
        'mes': mes,
        'semana': semana,
    }

    return render(request, "pages/carteiras/index.html", context={"carteiras": carteiras, "totais": totais})


def carteira(request: WSGIRequest, nome_carteira: str):
    carteira = Carteira.find_by_name(nome=nome_carteira)
    operacoes = Operacao.filter_by_carteira(carteira_id=carteira.id)
    carteira = CarteiraService.summarize(carteira, operacoes)
    context = {'carteira': carteira, 'operacoes': operacoes}
    return render(request, "pages/carteiras/carteira.html", context=context)
