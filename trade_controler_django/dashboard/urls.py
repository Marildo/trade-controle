"""
Created on 08/03/2022
by MarildoCesar
"""

from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('upload_notas_corretagem', views.upload_notas_corretagem, name='upload_notas_corretagem')
]
