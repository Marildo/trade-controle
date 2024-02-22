# @author Marildo Cesar 09/02/2024

from flask import Blueprint, request

from .rest_response import format_response

from ...controller import BacktestController, AtivoController

name = 'AtivosRouter'
resource = '/ativos'
ativos_router = Blueprint(name=name, import_name=name, url_prefix=resource)


@ativos_router.route('', methods=['GET'])
@format_response
def ativos():
    return AtivoController.readAll()


