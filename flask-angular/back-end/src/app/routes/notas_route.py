"""
 @author Marildo Cesar 06/05/2023
"""
from flask import Blueprint, request

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
                data = dict(status=ex.message, id=ex.id, file=file.filename)
        else:
            data = dict(status='Extensão inválida', id="", file=file.filename)

        result.append(data)
        i += 1
        file_item = f'file{i}'
        has_file = file_item in request.files

    return result


@nota_router.route('/arquivos/<int:_id>', methods=['PUT', 'PATCH'])
@format_response
def file_proccess(_id: int):
    map_controller = {'PUT': NotaController.process_nota, 'PATCH': NotaController.reprocess_nota}
    return map_controller[request.method](_id)


@nota_router.route('/arquivos/infocomp', methods=['PUT'])
@format_response
def addd_info_complementares():
    return NotaController.add_info_complementares()


@nota_router.route('/arquivos/search', methods=['PUT'])
@format_response
def search_files():
    return NotaController.search_corretagens()


@nota_router.route('/arquivos/pdf/<int:_id>', methods=['GET'])
@format_response
def download_pdf(_id: int):
    return NotaController.get_pdf(_id)
