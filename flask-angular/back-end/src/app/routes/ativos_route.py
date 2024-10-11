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


@ativos_router.route('', methods=['POST'])
@format_response
def register():
    return AtivoController.register()


@ativos_router.route('', methods=['PUT'])
@format_response
def load_fd():
    return AtivoController.load_fundamental_data()


@ativos_router.route('/top_by_fundamentals', methods=['GET'])
@format_response
def get_top():
    return AtivoController.get_top_by_fundamentals()
