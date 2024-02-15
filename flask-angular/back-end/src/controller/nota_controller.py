"""
 @author Marildo Cesar 06/05/2023
"""

from typing import List
from datetime import datetime
from pathlib import Path

from flask import request
from webargs.flaskparser import parser
from webargs import fields

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from ..exceptions import EmptyFileException
from ..settings import config
from ..model.enums import NotaStatusProcess, TipoNota
from ..model import FileCorretagem, NotaCorretagem
from ..exceptions import DuplicationProcessingException

from ..services import ReadPDFCorretagem, ToroService
from ..utils.dict_util import rows_to_dicts
from ..utils.str_util import capitalize_plus

from .schemas import ArquivoSchema
from .operacoes_controller import OperacaoController


class NotaController:

    @classmethod
    def store_pdf(cls, file: FileStorage):
        today = datetime.today()
        file_corr = FileCorretagem(name=file.filename, data_upload=today, status=NotaStatusProcess.AGUARDANDO,
                                   tipo=TipoNota.NA)

        stored = file_corr.is_exists()
        if stored:
            if stored.status in (NotaStatusProcess.ERROR, NotaStatusProcess.PROCESSANDO):
                return cls.process_nota(stored.id)
            else:
                raise DuplicationProcessingException(stored.id)

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

        if filecorr.status is NotaStatusProcess.PROCESSANDO:
            diff = (datetime.today() - filecorr.data_processamento).seconds / 60
            if diff < 0.3:  # TODO VOLTA O LIMITE
                raise BadRequest(
                    'Arquivo já está processando, aguarde o final do processamento ou tente novamente' + f' em  {3 - int(diff)} minutos'
                )

        if filecorr.status is NotaStatusProcess.FINALIZADO:
            return NotaController.load_notas(file_id)

        return cls.__process_notas(filecorr, file_id)

    @classmethod
    def __load_notas_from_arquivos(cls, filecorr: FileCorretagem):
        filecorr.status = NotaStatusProcess.PROCESSANDO
        filecorr.data_processamento = datetime.today()
        filecorr.update()
        sufix = filecorr.data_upload.strftime('__%Y_%m_%d_%H_%M')
        filename = filecorr.name.replace('.pdf', f'{sufix}.pdf')
        path_file = str(Path(config.get_path_notas()).joinpath(filename))
        reader = ReadPDFCorretagem()
        reader.read(path_file)
        notas = reader.notas()
        total_operacoes = sum([len(n.operacoes) for n in notas])
        if total_operacoes == 0:
            raise EmptyFileException("Nota inválida")
        for n in notas:
            n.file = filecorr
        return notas

    @classmethod
    def __process_notas(cls, filecorr: FileCorretagem, file_id):
        try:
            notas = cls.__load_notas_from_arquivos(filecorr)
            OperacaoController.save_operacoes(notas)
            if notas:
                filecorr.status = NotaStatusProcess.FINALIZADO
                filecorr.tipo = notas[0].tipo_nota
                filecorr.data_processamento = datetime.today()
                filecorr.update()

            return cls.load_notas(file_id)
        except EmptyFileException as ex:
            filecorr.detele()
            raise ex
        except Exception as ex:
            filecorr.status = NotaStatusProcess.ERROR
            filecorr.update()
            raise ex

    @classmethod
    def reprocess_nota(cls, file_id: int):
        filecorr = FileCorretagem().read_by_id(file_id)
        # reference_date = filecorr.notas[0].data_referencia

        return cls.__process_notas(filecorr, file_id)

    @staticmethod
    def read_by_params() -> List:
        input_schema = {
            'tipo': fields.Int(),
            'start_referencia': fields.Date(),
            'end_referencia': fields.Date(),
            'start_processamento': fields.Date(),
            'end_processamento': fields.Date(),
        }
        args = parser.parse(input_schema, request, location='querystring')
        data = FileCorretagem.list_arquivos(args)
        data = rows_to_dicts(data)
        response = []
        for item in data:
            for k, v in item.items():
                if k in ('tipo', 'status'):
                    item[k] = capitalize_plus(v)
            response.append(item)
        return response

    @staticmethod
    def load_notas(file_id):
        data = FileCorretagem().read_by_id(file_id)
        if not data:
            raise BadRequest(f'Id {file_id} não encontrado')

        response = ArquivoSchema().dump(data)
        return response

    @classmethod
    def search_corretagens(cls) -> dict:
        notas = []
        start_date = NotaCorretagem.get_last_date_processed()[0]
        # start_date = datetime.today().replace(day=25).date()
        service = ToroService()
        files = service.process_corretagem(start_date)
        for file in files:
            try:
                resp = cls.store_pdf(file)
                data = dict(status=resp['status'], file=file.filename, id=resp['id'])
            except DuplicationProcessingException as ex:
                data = dict(status=ex.message, id=ex.id, file=file.filename)
            notas.append(data)

        return {
            'numero_notas': len(notas),
            'notas': notas
        }
