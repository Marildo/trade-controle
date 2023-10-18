# @author Marildo Cesar 17/10/2023

from flask import Blueprint, request

from src.exceptions import DuplicationProcessingException
from .rest_response import format_response
from ...controller import CarteiraController

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