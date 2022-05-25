from django.core.files.storage import FileSystemStorage
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from services.read_pdf_corretagem import  ReadPDFCorretagem


def index(request: WSGIRequest):
    return render(request, 'pages/index.html')


def upload_notas_corretagem(request: WSGIRequest):
    file = request.FILES['corretagem']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded = fs.url(filename)

    file_name: str = "C:/Users/Cesar/Downloads/nota-acoes-2022_04_08.pdf"
    file_name = 'C:/Users/Cesar/Downloads/nota-futuro-2022_04_29.pdf'
    ready = ReadPDFCorretagem()
    operacoes = ready.read(file_name)
    print(ready.data_operacao)
    print(ready.operacoes)

    return HttpResponse(uploaded)
