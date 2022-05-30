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
    return render(request, 'pages/index.html')
