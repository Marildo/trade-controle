from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


def index(request: WSGIRequest):
    return render(request, 'pages/index.html')

def upload_notas_corretagem(request: WSGIRequest):
    file = request.FILES['corretagem']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded = fs.url(filename)
    return HttpResponse(uploaded)
