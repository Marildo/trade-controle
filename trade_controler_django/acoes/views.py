from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from services.status_invest import StatusInvest
from .models import Acao


def index(request: WSGIRequest):
    acoes = Acao.objects.all()
    return render(request, "pages/acoes/acoes.html", context={"acoes": acoes})


def acao(request: WSGIRequest, codigo: str):
    _acao = Acao.objects.filter(codigo=codigo.upper()).first()
    return render(request, "pages/acoes/acao.html", context={"acao": _acao})


def search(request: WSGIRequest):
    nome: str = request.GET.get("ativo")
    acoes = Acao.search(value=nome.upper())
    if not acoes:
        service = StatusInvest()
        acoes = service.find_by_name(nome)
        if not acoes:
            messages.add_message(request=request, level=messages.ERROR, message="Ativo não econtrado")
            return redirect("acoes")

        for acao in acoes:
            acao.setor.save()
            acao.subsetor.save()
            acao.segmento.save()
            acao.save()
            service.download_images(acao)

    return render(request, "pages/acoes/acao.html", context={"acoes": acoes})
