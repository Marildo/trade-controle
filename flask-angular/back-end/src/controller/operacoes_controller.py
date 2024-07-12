"""
 @author Marildo Cesar 25/04/2023
"""

from datetime import date, timedelta, datetime
from typing import Dict, List
import csv

import gspread
from flask import request
from webargs import fields
from webargs import validate
from webargs.flaskparser import parser
import statistics

from werkzeug.exceptions import BadRequest

from .carteira_controller import CarteiraController
from .importador_nota import ImportadorNota
from ..model import Operacao, Historico, Setup
from ..model.dtos import Nota
from ..services import YFinanceService
from ..settings import logger, config
from ..utils.dict_util import rows_to_dicts


class OperacaoController:
    operations = List[Dict]

    @classmethod
    def save_operacoes(cls, notas: List[Nota]):
        ImportadorNota.import_notas(notas)
        cls.update_historico()
        CarteiraController.update_saldos()

        logger.info('Finished import')

    @classmethod
    def update_operacao(cls):
        input_schema = {
            'id': fields.Int(required=True),
            'ativo': fields.String(required=False),
            'ativo_id': fields.Int(required=True),
            'carteira': fields.String(required=False, allow_none=True),
            'carteira_id': fields.Int(required=True),
            'data_compra': fields.Date(required=False, allow_none=True),
            'data_encerramento': fields.Date(required=False, allow_none=True),
            'data_venda': fields.Date(required=False, allow_none=True),
            'custos': fields.Float(required=False),
            'pm_compra': fields.Float(required=False),
            'pm_venda': fields.Float(required=False),
            'qtd_compra': fields.Float(required=False),
            'qtd_venda': fields.Float(required=False),
            'resultado': fields.Float(required=False),
            'irpf': fields.Float(required=False),
            'compra_venda': fields.Str(required=False),
            'nota_compra': fields.Int(required=False, allow_none=True),
            'nota_venda': fields.Int(required=False, allow_none=True),
            'nota_compra_id': fields.Int(required=False, allow_none=True),
            'nota_venda_id': fields.Int(required=False, allow_none=True),
            'compra_hist_id': fields.Int(required=False, allow_none=True),
            'venda_hist_id': fields.Int(required=False, allow_none=True),
            'setup_id': fields.Int(required=False, allow_none=True),
            'setup': fields.Str(required=False, allow_none=True),
            'encerrada': fields.Bool(required=False),
            'daytrade': fields.Bool(required=False),
            'tendencia': fields.Str(required=False),
            'contexto': fields.Bool(required=False),
            'segui_plano': fields.Bool(required=False),
            'payoff': fields.Float(required=False),
            'quality': fields.Float(required=False),
            'obs': fields.Str(required=False, allow_none=True),
        }
        args = parser.parse(input_schema, request, location='json')
        del args['ativo']
        del args['carteira']
        del args['nota_compra']
        del args['nota_venda']
        del args['setup']
        operacao = Operacao(**args)
        operacao.update()
        return {'status': 'Atualização realizada com sucesso'}

    @classmethod
    def fetch_detail(cls):
        input_schema = {
            'id': fields.Int(),
            'start_data_compra': fields.Date(),
            'end_data_compra': fields.Date(),
            'start_data_venda': fields.Date(),
            'end_data_venda': fields.Date(),
            'start_encerramento': fields.Date(),
            'end_encerramento': fields.Date(),
            'ativo_id': fields.Int(),
            'nota_compra': fields.Int(),
            'nota_venda': fields.Int(),
            'file_id': fields.Int(),
            'encerrada': fields.Bool(),
            'daytrade': fields.Bool(),
            'codigo': fields.Str(),
            'carteira_id': fields.Int(),
            'tipo_investimento': fields.Int(),
        }
        args = parser.parse(input_schema, request, location='querystring')
        data = Operacao.fetch_detail(args)
        custos = sum([i.custos for i in data])
        irpf = sum([i.irpf for i in data])
        numero_operacoes = len(data)
        items = rows_to_dicts(data)
        total = sum([i.resultado for i in data])
        liquido = total - (custos + irpf)
        quality = round(statistics.mean([i.quality for i in data]), 2)
        response = dict(items=items,
                        summary=dict(resultado=total, liquido=liquido, custos=custos, irpf=irpf,
                                     numero_operacoes=numero_operacoes, quality=quality))
        return response

    @classmethod
    def fetch_summary(cls):
        input_schema = {'ativo_id': fields.Int()}
        args = parser.parse(input_schema, request, location='querystring')
        data = Operacao.fetch_summary(args)
        numero_operacoes = len(data)
        items = rows_to_dicts(data)
        resultado = sum([i.resultado for i in data])
        total = sum([i.cotacao * i.qtd for i in data])
        response = dict(items=items, summary=dict(resultado=resultado, numero_operacoes=numero_operacoes, total=total))
        return response

    @classmethod
    def fetch_dashboard_data(cls):
        totais = Operacao.fetch_summary_total(True)
        group_quarter = Operacao.fetch_summary_quarter_daytrade()
        daytrade_operations = dict(group_trimestral=rows_to_dicts(group_quarter),
                                   total_mensal=totais.mensal or 0,
                                   total_semanal=totais.semanal or 0,
                                   total_anual=totais.anual or 0,
                                   total_acumulado=totais.acumulado or 0)

        totais = Operacao.fetch_summary_total(False)
        long_operations = dict(
            total_mensal=totais.mensal or 0,
            total_semanal=totais.semanal or 0,
            total_anual=totais.anual or 0,
            total_acumulado=totais.acumulado or 0)

        response = dict(daytrade_operations=daytrade_operations, long_operations=long_operations)
        return response

    @classmethod
    def fetch_statistics_daytrade(cls):
        input_schema = {'period_type': fields.Int(required=True, validate=validate.Range(min=1, max=5))}
        args = parser.parse(input_schema, request, location='querystring')

        today = date.today() - timedelta(days=1)
        period_type_map = {
            1: date(day=1, month=1, year=2000),
            2: today.replace(day=1, month=1),
            3: today.replace(day=1),
            4: today - timedelta(days=today.weekday()),
            5: today if today.weekday() not in (5, 6) else today - timedelta(days=(today.weekday() - 4) % 7),
        }

        start_date = period_type_map[int(args['period_type'])]
        operations = Operacao.fetch_daytrade_operations(start_date)
        statistics = Operacao.fetch_statistics_daytrade(start_date)
        st = rows_to_dicts(statistics)[0]
        response = dict(operacoes=rows_to_dicts(operations), statistics=st)
        return response

    @classmethod
    def update_prices(cls):
        def dif_time(dt0, dt1):
            diff = dt0 - dt1
            time_diff = diff.total_seconds() / 3600
            return time_diff

        operacoes = Operacao().read_by_params(dict(encerrada=False, daytrade=False))
        ativos = list(set([o.ativo for o in operacoes]))
        ativos = [i for i in ativos if dif_time(datetime.today(), i.update_at) > 1]
        if ativos:
            yfinance = YFinanceService()
            try:
                yfinance.update_price(ativos)
                for at in ativos:
                    at.save()
                    for item in [o for o in operacoes if o.ativo == at]:
                        item.resultado = item.calc_resultado()
                        item.save()
            except Exception as ex:
                logger.error(ex)

    @classmethod
    def update_historico(cls):
        param = dict(compra_hist_id=None, venda_hist_id=None)
        operacoes = Operacao().read_by_params(param)

        for op in operacoes:
            if op.carteira_id is None:
                continue
            if op.daytrade:
                hist = Historico()
                hist.carteira_id = op.carteira_id
                hist.descricao = f'Daytrade de {op.ativo.codigo}'
                hist.valor = op.resultado - op.custos - op.irpf
                hist.data_referencia = op.data_compra
                hist.save()
                op.compra_hist_id = hist.id
                op.venda_hist_id = hist.id
            else:
                if op.data_compra is not None:
                    hist = Historico()
                    hist.carteira_id = op.carteira_id
                    hist.data_referencia = op.data_compra
                    hist.descricao = f'Compra de {op.ativo.codigo}'
                    custos = 0 if op.compra_venda == 'COMPRA' else op.custos - op.irpf
                    hist.valor = -1 * op.pm_compra * op.qtd_compra - custos
                    hist.save()
                    op.compra_hist_id = hist.id

                if op.data_venda is not None:
                    hist = Historico()
                    hist.carteira_id = op.carteira_id
                    hist.data_referencia = op.data_venda
                    hist.descricao = f'Venda de {op.ativo.codigo}'
                    custos = 0 if op.compra_venda == 'VENDA' else op.custos - op.irpf
                    hist.valor = op.pm_venda * op.qtd_venda - custos
                    hist.save()
                    op.compra_hist_id = hist.id

            op.save()

    @classmethod
    def update_info_complementares(cls, data):
        infos = data['info'].split('\n')
        header = infos[0].split(';')
        infos = infos[1:]

        infos_list = []
        for i in range(len(infos)):
            row = infos[i].split(';')
            if len(row) < 2:
                continue

            row_dict = {}
            for h in range(len(header)):
                row_dict[header[h].lower()] = row[h]

            row_dict['processed'] = False
            infos_list.append(row_dict)

        operacoes = Operacao().find_by_file_id(data['file_id'])
        setups = Setup().read_by_params({})

        def find_value(field: str, info_row: Dict):
            field = field.lower()
            value = info_row.get(field, None)
            if field == 'setup':
                items = [s for s in setups if s.nome == value]
                value = items[0].id if items else 0
            elif field == 'resultado':
                value = float(value.replace('R$', ''))
            elif field == 'tendência':
                value = value.upper()
            elif field == 'payoff':
                value = float(value)
            elif field in ('contexto', 'segui o plano'):
                value = value == 'Sim'

            return value

        i = 0
        for info in infos_list:
            oper = operacoes[i]
            resultado = find_value('resultado', info)
            if oper.resultado == resultado:
                oper.setup_id = find_value('Setup', info)
                oper.tendencia = find_value('Tendência', info)
                oper.segui_plano = find_value('Segui o Plano', info)
                oper.contexto = find_value('Contexto', info)
                oper.payoff = find_value('Payoff', info)
                oper.obs = find_value('Obs', info)
                oper.calc_quality()
                oper.save()
                info['processed'] = True

            i += 1

        operacoes = [o for o in operacoes if o.setup_id is None]
        infos_np = [i for i in infos_list if i['processed'] is False]
        for oper in operacoes:
            infs = [i for i in infos_np if find_value('resultado', i) == oper.resultado]
            if len(infs) == 1:
                info = infs[0]
                oper.setup_id = find_value('Setup', info)
                oper.tendencia = find_value('Tendência', info)
                oper.segui_plano = find_value('Segui o Plano', info)
                oper.contexto = find_value('Contexto', info)
                oper.payoff = find_value('Payoff', info)
                oper.obs = find_value('Obs', info)
                oper.calc_quality()
                oper.save()

    @classmethod
    def update_info_complementares_from_sheet(cls, file_id: int):
        credential = config.get_path_google_credential()
        gc = gspread.service_account(filename=credential)
        try:
            url = config.get_path_google_url()
            sheet = gc.open_by_url(url).worksheet('Daytrade')
        except ConnectionError:
            raise BadRequest('Falha ao conectar no google sheets')

        dados = sheet.get_all_values()
        header = [i.lower() for i in dados[11]]
        dados = [i for i in dados[12:-1] if i[0] != '']

        operacoes = Operacao().find_by_file_id(file_id)
        setups = Setup().read_by_params({})

        def find_value(field: str, row: List):
            field = field.lower()
            index = header.index(field)
            value = row[index]
            if field == 'setup':
                items = [s for s in setups if s.nome == value]
                value = items[0].id if items else 0
            elif field == 'resultado':
                value = float(value.replace('R$', ''))
            elif field == 'tendência':
                value = value.upper()
            elif field == 'payoff':
                value = float(value)
            elif field in ('contexto', 'segui o plano'):
                value = value == 'Sim'

            return value

        not_processed = []
        i = 0
        for info in dados:
            oper = operacoes[i]
            resultado = find_value('resultado', info)
            ativo = find_value('ativo', info)
            if oper.resultado == resultado and ativo == oper.ativo.codigo:
                oper.setup_id = find_value('Setup', info)
                oper.tendencia = find_value('Tendência', info)
                oper.segui_plano = find_value('Segui o Plano', info)
                oper.contexto = find_value('Contexto', info)
                oper.payoff = find_value('Payoff', info)
                oper.obs = find_value('Obs', info)
                oper.calc_quality()
                oper.save()
            else:
                not_processed.append(info)

            i += 1

        operacoes = [o for o in operacoes if o.setup_id is None]
        for oper in operacoes:
            infs = [i for i in not_processed if
                    find_value('resultado', i) == oper.resultado and find_value('ativo', i) == oper.ativo.codigo]
            if len(infs) == 1:
                info = infs[0]
                oper.setup_id = find_value('Setup', info)
                oper.tendencia = find_value('Tendência', info)
                oper.segui_plano = find_value('Segui o Plano', info)
                oper.contexto = find_value('Contexto', info)
                oper.payoff = find_value('Payoff', info)
                oper.obs = find_value('Obs', info)
                oper.calc_quality()
                oper.save()
