"""
 @author Marildo Cesar 06/05/2023
"""
import threading
import time
from typing import List
from datetime import datetime
from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest, NotFound

from src.settings import config
from src.model.enums import NotaStatusProcess
from src.model import FileCorretagem, NotaCorretagem

from src.services import ReadPDFCorretagem

from .schemas import NotaSchema
from .operacoes import OperacaoController


class NotaController:

    @staticmethod
    def store_pdf(file: FileStorage):
        today = datetime.today()
        file_corr = FileCorretagem(name=file.filename, data_upload=today, status=NotaStatusProcess.ARGUARDANDO)

        if file_corr.is_exists():
            raise BadRequest('Arquivo de corretagem ja foi importada, aguarde o final do processamento.')

        sufix = today.strftime('__%Y_%m_%d_%H_%M_%S')
        filename = file.filename.replace('.pdf', f'{sufix}.pdf')
        path_file = Path(config.get_path_notas()).joinpath(filename)
        file.save(path_file)
        file_corr.save()

    @staticmethod
    def process_nota(nota_id: int):
        filecorr = FileCorretagem().read_by_id(nota_id)
        if not filecorr:
            raise BadRequest(f'Id {nota_id} não encontrado')

        try:
            filecorr.status = NotaStatusProcess.PROCESSANDO
            filecorr.save()

            sufix = filecorr.data_upload.strftime('__%Y_%m_%d_%H_%M_%S')
            filename = filecorr.name.replace('.pdf', f'{sufix}.pdf')
            path_file = str(Path(config.get_path_notas()).joinpath(filename))
            reader = ReadPDFCorretagem()
            reader.read(path_file)
            notas = reader.notas()
            for n in notas:
                n.file = filecorr

            OperacaoController.save_operacoes(notas)
            filecorr.tipo = notas[0].tipo_nota
            filecorr.status = NotaStatusProcess.FINALIZAD0
            filecorr.data_processamento = datetime.today()
            filecorr.save()
        except Exception as ex:
            filecorr.status = NotaStatusProcess.ERROR
            filecorr.save()
            raise ex

    @staticmethod
    def read_by_params(params) -> List:
        data = FileCorretagem.read_by_params(params)
        response = NotaSchema().dump(data, many=True)
        return response
