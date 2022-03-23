from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from .models import Carteira


def index(request: WSGIRequest):
    carteiras =  Carteira.objects.all()
    return render(request, "pages/carteiras/index.html", context={"carteiras": carteiras})
