"""
Created on 09/03/2022
by MarildoCesar
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='acoes'),
    path('/buscar', views.search, name='search'),
]