"""
 @author Marildo Cesar 06/05/2023
"""

from typing import List
from datetime import datetime
from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from model.enums import NotaStatusProcess
from src.model import NotaCorretagem

from .schemas import NotaSchema
from src.settings import config


class NotaController:

    @staticmethod
    def store_pdf(file: FileStorage):
        today = datetime.today()
        nota = NotaCorretagem(pdf_name=file.filename, data_upload=today, status=NotaStatusProcess.ARGUARDANDO)

        if nota.is_exists():
            raise BadRequest('Nota de corretagem ja foi importada, aguarda o final do processamento')

        sufix = today.strftime('__%Y_%m_%d_%H_%M_%S')
        filename = file.filename.replace('.pdf', f'{sufix}.pdf')
        path_file = Path(config.get_path_notas()).joinpath(filename)
        file.save(path_file)
        nota.save()

    @staticmethod
    def read_by_params(params) -> List:
        data = NotaCorretagem.read_by_params(params)
        response = NotaSchema().dump(data, many=True)
        return response
