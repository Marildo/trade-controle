"""
 @author Marildo Cesar 10/05/2023
"""
from flask import Blueprint, make_response, request
from werkzeug.exceptions import BadRequest

from .rest_response import format_response
from src.controller import OperacaoController

name = 'OperacoesRouter'
resource = '/operacoes'
operacao_router = Blueprint(name=name, import_name=name, url_prefix=resource)


@operacao_router.route('/', methods=['GET'])
@format_response
def load_dashboard_data():
    return OperacaoController.fetch_dashboard_data()


@operacao_router.route('/summary/', methods=['GET'])
@format_response
def load_opened():
    return OperacaoController.fetch_summary()


@operacao_router.route('/detail/', methods=['GET'])
@format_response
def load_closed():
    return OperacaoController.fetch_detail()
