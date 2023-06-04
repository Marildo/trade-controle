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


@operacao_router.route('/closed/', methods=['GET'])
@format_response
def load_closed():
    return OperacaoController.fetch_closed()


@operacao_router.route('/opened/', methods=['GET'])
@format_response
def load_opened():
    return OperacaoController.fetch_not_closed()
