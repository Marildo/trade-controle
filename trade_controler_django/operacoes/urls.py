"""
Created on 22/03/2022
by MarildoCesar
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='operacoes'),
    path('upload_notas_corretagem', views.upload_notas_corretagem, name='upload_notas_corretagem')
]
