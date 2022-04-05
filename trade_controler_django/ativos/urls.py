"""
Created on 09/03/2022
by MarildoCesar
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='ativos'),
    path('busca/', views.search, name='search'),
    path('update_prices/', views.update_prices, name='update_prices'),
    path('<slug:codigo>/', views.ativo, name='ativo'),
]
