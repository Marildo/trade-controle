from django.core.files.storage import FileSystemStorage
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def index(request: WSGIRequest):
    return render(request, 'pages/index.html')


def upload_notas_corretagem(request: WSGIRequest):
    file = request.FILES['corretagem']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded = fs.url(filename)
    return HttpResponse(uploaded)
