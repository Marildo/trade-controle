from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def index(request: WSGIRequest):
    return render(request, 'pages/acoes.html')


def search(request: WSGIRequest):
    codigo = request.GET.get('nome')
    df = locate_cotacao(codigo)
    result = f"{df['Adj Close']} "
    return HttpResponse(result)


def locate_cotacao(codigo:str):
    import yfinance as yf
    import pandas as pd

    precos = pd.DataFrame()
    precos[0]= yf.download('VALE3.SA', start='2022-03-09', end='2022-03-10')
    return precos