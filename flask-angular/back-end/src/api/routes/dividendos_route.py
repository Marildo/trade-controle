# @author Marildo Cesar 24/09/2023

from flask import Blueprint, request

from .rest_response import format_response
from src.controller import DividendosController

name = 'DivendedoRouter'
resource = '/dividendos'
dividendo_router = Blueprint(name=name, import_name=name, url_prefix=resource)


@dividendo_router.route('/', methods=['GET'])
@format_response
def summary():
    return DividendosController.summary()


@dividendo_router.route('/process', methods=['PUT'])
@format_response
def process():
    DividendosController.proccess()
