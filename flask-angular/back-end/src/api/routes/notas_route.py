"""
 @author Marildo Cesar 06/05/2023
"""
from flask import Blueprint, make_response, request
from werkzeug.exceptions import BadRequest

from src.exceptions import DuplicationProcessingException
from .rest_response import format_response
from src.controller import NotaController

name = 'NotasRouter'
resource = '/notas'
nota_router = Blueprint(name=name, import_name=name, url_prefix=resource)


@nota_router.route('/arquivos', methods=['GET'])
@format_response
def file_list():
    return NotaController.read_by_params()


@nota_router.route('/arquivos/<int:_id>', methods=['GET'])
@format_response
def load_notas(_id: int):
    return NotaController.load_notas(_id)


@nota_router.route('/arquivos', methods=['POST'])
@format_response
def file_upload():
    i = 1
    file_item = f'file{i}'
    has_file = file_item in request.files
    result = []
    while has_file:
        file = request.files[file_item]
        if file.filename != '' and file.mimetype.endswith('/pdf'):
            try:
                resp = NotaController.store_pdf(file)
                data = dict(status=resp['status'], file=file.filename, id=resp['id'])
            except DuplicationProcessingException as ex:
                data = dict(status=ex.message, id=ex.id, file=file.filename, )
        else:
            data = dict(status='Extensão inválida', id="", file=file.filename)

        result.append(data)
        i += 1
        file_item = f'file{i}'
        has_file = file_item in request.files

    return result


@nota_router.route('/arquivos/<int:_id>', methods=['PUT'])
@format_response
def file_proccess(_id: int):
    return NotaController.process_nota(_id)
