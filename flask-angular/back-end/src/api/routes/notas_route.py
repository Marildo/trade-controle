"""
 @author Marildo Cesar 06/05/2023
"""
from flask import Blueprint, make_response, request
from werkzeug.exceptions import BadRequest

from .rest_response import format_response
from src.controller import NotaController

name = 'NotasRouter'
resource = '/notas'
nota_router = Blueprint(name=name, import_name=name, url_prefix=resource)


@nota_router.route('/', methods=['GET'])
@format_response
def index():
    return NotaController.read_by_params({})


@nota_router.route('/upload', methods=['POST'])
@format_response
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            raise BadRequest('Nenhum arquivo enviado')
        file = request.files['file']
        if file.filename == '':
            raise BadRequest('Nenhum arquivo selecionado')
        if not file.mimetype.endswith('/pdf'):
            raise BadRequest('Apenas arquivos PDF são permitidos')

        NotaController.store_pdf(file)
