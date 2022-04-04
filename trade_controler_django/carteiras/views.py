from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render

from operacoes.models import Operacao
from services.carteira_service import CarteiraService
from services.yfinance_service import YFinanceService
from .models import Carteira


def index(request: WSGIRequest):
    carteiras = Carteira.objects.all()
    return render(request, "pages/carteiras/index.html", context={"carteiras": carteiras})


def carteira(request: WSGIRequest, nome_carteira: str):
    carteira = Carteira.find_by_name(nome=nome_carteira)
    operacoes = Operacao.filter_by_carteira(carteira_id=carteira.id)
    carteira = CarteiraService.summarize(carteira, operacoes)
    context = {'carteira': carteira, 'operacoes': operacoes}
    return render(request, "pages/carteiras/carteira.html", context=context)


def update_carteira(request: WSGIRequest, id: int):
    operacoes = Operacao.filter_by_carteira(carteira_id=id)
    ativos = [item.ativo for item in operacoes]
    YFinanceService.update_price(ativos)
    return JsonResponse({"res": "ok"})
