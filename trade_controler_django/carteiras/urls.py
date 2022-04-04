"""
Created on 17/03/2022
by MarildoCesar
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='carteiras'),
    path('update/<slug:id>', views.update_carteira, name='update_carteira'),
    path('<slug:nome_carteira>/', views.carteira, name='carteira'),
]
