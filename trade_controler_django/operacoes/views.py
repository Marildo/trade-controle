from django.shortcuts import render

from django.core.handlers.wsgi import WSGIRequest
from django.core.files.storage import FileSystemStorage
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from services.corretagem.read_pdf_corretagem import ReadPDFCorretagem
from pathlib import Path
from operacoes.models import Operacao
from ativos.models import Ativo
from carteiras.models import Carteira


def index(request: WSGIRequest):
    return render(request, 'pages/operacoes/index.html')


def upload_notas_corretagem(request: WSGIRequest):
    # TODO - Salvar nomes de arquivos processados
    file = request.FILES['corretagem']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    full_name = str(Path(fs.location).joinpath(filename))
    ready = ReadPDFCorretagem()
    ready.read(full_name)
    data = ready.operacoes()

    operacoes = []
    for item in data:
        ativo = Ativo.search(item['ativo']).first()
        del item['ativo']

        operacao = Operacao(ativo=ativo)
        for field in operacao._meta.get_fields():
            if field.name in item:
                setattr(operacao, field.name, item[field.name])

        daytrade = item['qtd_compra'] == item['qtd_venda']
        operacao.daytrade = daytrade
        if daytrade:
            operacao.encerrada = True
            operacao.quantidade = item['qtd_compra']
            operacao.carteira = Carteira.find_of_daytrade()
            operacao.data_encerramento = operacao.data_compra

        operacao.save()
        operacoes.append(operacao)

    return render(request, "pages/operacoes/index.html", context={'operacoes': operacoes})
