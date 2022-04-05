from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect

from services.status_invest import StatusInvest
from services.yfinance_service import YFinanceService
from .models import Ativo


def index(request: WSGIRequest):
    tipo: str = request.GET.get("tipo")
    if tipo:
        ativos = Ativo.objects.filter(tipo=tipo).all()
    else:
        ativos = Ativo.objects.filter().all()
    return render(request, "pages/ativos/index.html", context={"ativos": ativos})


def ativo(request: WSGIRequest, codigo: str):
    ativos = Ativo.objects.filter(codigo=codigo.upper()).all()
    return render(request, "pages/ativos/view.html", context={"ativos": ativos})


def search(request: WSGIRequest):
    nome: str = request.GET.get("ativo")
    ativos = Ativo.search(value=nome.upper())
    if not ativos:
        service = StatusInvest()
        ativos = service.find_by_name(nome)
        if not ativos:
            messages.add_message(request=request, level=messages.ERROR, message="Ativo não econtrado")
            return redirect("ativos")

        for ativo in ativos:
            ativo.setor.save()
            ativo.subsetor.save()
            ativo.segmento.save()
            ativo.save()
            service.download_images(ativo)

    return render(request, "pages/ativos/view.html", context={"ativos": ativos})


def update_prices(request: WSGIRequest):
    ativos = Ativo.objects.filter().all()
    YFinanceService.update_price(ativos)
    return JsonResponse({"res": "ok"})
