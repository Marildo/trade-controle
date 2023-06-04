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

from .schemas import ArquivoSchema
from .operacoes_controller import OperacaoController


class NotaController:

    @classmethod
    def store_pdf(cls, file: FileStorage):
        today = datetime.today()
        file_corr = FileCorretagem(name=file.filename, data_upload=today, status=NotaStatusProcess.ARGUARDANDO)

        if file_corr.is_exists():
            raise BadRequest('Arquivo de corretagem ja foi importada, aguarde o final do processamento.')

        sufix = today.strftime('__%Y_%m_%d_%H_%M')
        filename = file.filename.replace('.pdf', f'{sufix}.pdf')
        path_file = Path(config.get_path_notas()).joinpath(filename)
        file.save(path_file)
        file_corr.save()
        return cls.process_nota(file_corr.id)

    @classmethod
    def process_nota(cls, file_id: int):
        filecorr = FileCorretagem().read_by_id(file_id)
        if not filecorr:
            raise BadRequest(f'Id {file_id} não encontrado')

        # if filecorr.status is NotaStatusProcess.PROCESSANDO:
        #     diff = (datetime.today() - filecorr.data_processamento).seconds / 60
        #     if diff < 3:
        #         raise BadRequest(
        #             'Arquivo já está processando, aguarde o final do processamento ou tente novamente' +
        #             f'em  {3 - int(diff)} minutos'
        #         )

        if filecorr.status is NotaStatusProcess.FINALIZADO:
            return NotaController.load_notas(file_id)

        try:
            filecorr.status = NotaStatusProcess.PROCESSANDO
            filecorr.data_processamento = datetime.today()
            filecorr.update()

            sufix = filecorr.data_upload.strftime('__%Y_%m_%d_%H_%M')
            filename = filecorr.name.replace('.pdf', f'{sufix}.pdf')
            path_file = str(Path(config.get_path_notas()).joinpath(filename))
            reader = ReadPDFCorretagem()
            reader.read(path_file)
            notas = reader.notas()
            for n in notas:
                n.file = filecorr

            OperacaoController.save_operacoes(notas)

            filecorr.status = NotaStatusProcess.FINALIZADO
            filecorr.tipo = notas[0].tipo_nota
            filecorr.data_processamento = datetime.today()
            filecorr.update()

            return cls.load_notas(file_id)
        except Exception as ex:
            filecorr.status = NotaStatusProcess.ERROR
            filecorr.update()
            raise ex

    @staticmethod
    def read_by_params() -> List:
        data = FileCorretagem().read_by_params({})
        response = ArquivoSchema().dump(data, many=True)
        return response

    @staticmethod
    def load_notas(file_id):
        data = FileCorretagem().read_by_id(file_id)
        if not data:
            raise BadRequest(f'Id {file_id} não encontrado')

        response = ArquivoSchema().dump(data)
        return response
