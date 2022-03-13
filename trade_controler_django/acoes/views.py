from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from services.status_invest import StatusInvest
from .models import Acao


def index(request: WSGIRequest):
    return render(request, 'pages/acoes/acoes.html')


def search(request: WSGIRequest):
    nome: str = request.GET.get('nome')
    acao = Acao.objects.filter(nome=nome.upper()).first()
    if not acao:
        service = StatusInvest()
        acao = service.find_by_name(nome)
        acao.setor.save()
        acao.subsetor.save()
        acao.segmento.save()
        acao.save()

    return render(request, 'pages/acoes/acao.html', context={'acao': acao})
