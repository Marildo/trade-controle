# @author Marildo Cesar 17/10/2023

from flask import Blueprint, request

from .rest_response import format_response
from src.controller import CarteiraController

name = 'CarteiraRouter'
resource = '/carteiras'
carteira_router = Blueprint(name=name, import_name=name, url_prefix=resource)


@carteira_router.route('/', methods=['GET'])
@format_response
def carteiras():
    return CarteiraController.carteiras()


@carteira_router.route('/', methods=['POST'])
@format_response
def save():
    return CarteiraController.save()


@carteira_router.route('/', methods=['PUT'])
@format_response
def update():
    return CarteiraController.update()


@carteira_router.route('/movimentacoes', methods=['GET', 'POST'])
@format_response
def movimentaoes():
    map_controller = {
        'GET': CarteiraController.movimentacoes,
        'POST': CarteiraController.add_movimentacao
    }
    return map_controller[request.method]()


@carteira_router.route('/historicos', methods=['GET', 'POST'])
@format_response
def historicos():
    map_controller = {
        'GET': CarteiraController.historicos,
        'POST': CarteiraController.add_movimentacao
    }
    return map_controller[request.method]()
