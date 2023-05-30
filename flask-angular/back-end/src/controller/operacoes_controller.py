"""
 @author Marildo Cesar 25/04/2023
"""
from datetime import datetime, date
from json import dumps
from typing import Dict, List, Tuple
from collections import Counter

from flask import request
from webargs.flaskparser import parser
from webargs import fields, validate

from src.settings import logger
from src.utils.dict_util import rows_to_dicts
from src.model import db_connection, Operacao, NotaCorretagem, CompraVenda
from src.model.dtos import Nota
from .schemas import OperacaoSchema
from .ativos import AtivoController
from .query_validations import validate_group_by_operacoes


class OperacaoController:
    operations = List[Dict]

    @classmethod
    def save_operacoes(cls, notas: List[Nota]):
        ativos = set()
        for n in notas:
            for o in n.operacoes:
                ativos.add(o['ativo'])

        ativos = sorted(ativos)
        for item in ativos:
            AtivoController.find_by_or_save(item)

        for item in notas:
            cls.__import_nota(item)

        logger.info('Finished import')

    @classmethod
    def __import_nota(cls, item: Nota):
        map_order = {
            'C': lambda x: x.data_venda,
            'V': lambda x: x.data_compra,
        }
        today = datetime.today()
        session = db_connection.session
        try:
            nota_corr = NotaCorretagem(comprovante=item.comprovante,
                                       data_referencia=item.data_operacao, file_id=item.file.id)
            # if nota_corr.is_exists():
            #     logger.warn(f'Nota já foi importada ({nota_corr})')
            #     return

            # if nota_corr.comprovante in (45324,):                    print('Sfff')

            session.merge(nota_corr)
            session.flush()
            operacoes_nota = cls.__appoint_daytrade(item.operacoes)

            for op in operacoes_nota:
                tipo_operacao = op['tipo']
                logger.info(f'Store: Nota: {nota_corr} - op: {dumps(op)}')
                ativo = AtivoController.find_by_or_save(op['ativo'])

                # if ativo.id != 1030:
                #     continue
                #
                # logger.info(f'Store: Nota: {nota_corr} - op: {dumps(op)}')
                # print(f'{op["qtd"] * (1 if op["tipo"] == "C" else -1)}')

                c_v = CompraVenda.VENDA if tipo_operacao == 'C' else CompraVenda.COMPRA
                operacoes = Operacao.find_not_closed(ativo, c_v, op['daytrade'])

                if not operacoes:
                    operacao = cls.__new_operacao(op, nota_corr)
                    operacao.ativo = ativo
                    session.add(operacao)
                    session.flush()
                else:
                    if op['daytrade'] is False:
                        total_qtd = 0
                        if tipo_operacao == 'V':
                            filter_day = [i for i in operacoes if i.data_compra == nota_corr.data_referencia]
                            total_qtd = sum([i.qtd_compra for i in filter_day])
                        else:
                            filter_day = [i for i in operacoes if i.data_venda == nota_corr.data_referencia]
                            total_qtd = sum([i.qtd_venda for i in filter_day])

                        if total_qtd > op['qtd']:
                            operacoes = filter_day

                    if len(operacoes) > 1:
                        fd = []
                        if tipo_operacao == 'V':
                            fd = [i for i in operacoes if i.qtd_compra == op['qtd']]
                            if not fd:
                                fd = [i for i in operacoes if i.qtd_compra >= op['qtd']]
                        else:
                            fd = [i for i in operacoes if i.qtd_venda == op['qtd']]
                            if not fd:
                                fd = [i for i in operacoes if i.qtd_venda > op['qtd']]
                        if fd:
                            operacoes = [fd[0]]

                    operacoes.sort(key=map_order[tipo_operacao])
                    computed = 0
                    for row in operacoes:
                        if computed == op['qtd']:
                            continue
                        if tipo_operacao == 'V':
                            if row.qtd_compra <= op['qtd']:
                                row.qtd_venda = row.qtd_compra
                                row.pm_venda = op['preco']
                                row.custos = op['custos']
                                row.irpf = op['irpf']
                                row.nota_venda = nota_corr
                                row.data_venda = nota_corr.data_referencia
                                row.encerrada = True
                                row.daytrade = row.data_compra == row.data_venda
                                row.data_encerramento = row.data_venda
                                computed += row.qtd_compra
                            else:
                                new_op = cls.__copy_operacao(row)
                                new_op.qtd_venda = op['qtd']
                                new_op.qtd_compra = op['qtd']
                                new_op.pm_venda = op['preco']
                                new_op.custos = op['custos']
                                new_op.irpf = op['irpf']
                                new_op.nota_venda = nota_corr
                                new_op.data_venda = nota_corr.data_referencia
                                new_op.encerrada = True
                                new_op.data_encerramento = row.data_venda
                                new_op.daytrade = new_op.data_compra == new_op.data_venda
                                row.qtd_compra -= op['qtd']
                                computed += op['qtd']
                                session.add(new_op)
                        else:
                            if row.qtd_venda <= op['qtd']:
                                row.qtd_compra = row.qtd_venda
                                row.pm_compra = op['preco']
                                row.custos = op['custos']
                                row.irpf = op['irpf']
                                row.data_compra = nota_corr.data_referencia
                                row.nota_compra = nota_corr
                                row.encerrada = True
                                row.data_encerramento = row.data_compra
                                row.daytrade = row.data_compra == row.data_venda
                                computed += row.qtd_venda
                            else:
                                new_op = cls.__copy_operacao(row)
                                new_op.qtd_venda = op['qtd']
                                new_op.qtd_compra = op['qtd']
                                new_op.pm_compra = op['preco']
                                new_op.custos = op['custos']
                                new_op.irpf = op['irpf']
                                new_op.data_compra = nota_corr.data_referencia
                                new_op.nota_compra = nota_corr
                                new_op.encerrada = True
                                new_op.data_encerramento = row.data_compra
                                new_op.daytrade = new_op.data_compra == new_op.data_venda
                                row.qtd_venda -= op['qtd']
                                computed += op['qtd']
                                session.add(new_op)
                        session.add(row)
                        session.flush()

                    if computed > op['qtd']:
                        op['tipo'] = 'C'
                        operacao = cls.__new_operacao(op, nota_corr)
                        operacao.ativo = ativo
                        if tipo_operacao == 'V':
                            operacao.qtd_compra = computed - op['qtd']
                        else:
                            operacao.qtd_venda = computed - op['qtd']
                        session.add(operacao)
                    elif computed < op['qtd']:
                        op['tipo'] = 'V'
                        operacao = cls.__new_operacao(op, nota_corr)
                        operacao.ativo = ativo
                        if tipo_operacao == 'C':
                            operacao.qtd_compra = op['qtd'] - computed
                        else:
                            operacao.qtd_venda = op['qtd'] - computed
                        session.add(operacao)

                session.commit()
        except Exception as exep:
            logger.error(exep)
            session.rollback()
            raise exep

    @staticmethod
    def __appoint_daytrade(operacoes: operations):
        ativos = [i['ativo'] for i in operacoes]
        counter = Counter(ativos)
        single = [k for k, v in counter.items() if v == 1]
        for op in operacoes:
            op['daytrade'] = False if op['ativo'] in single else None

        ops = [i for i in operacoes if i['daytrade'] is None]
        ativos = set([i['ativo'] for i in ops])
        for item in ativos:
            ops_curr = [i for i in ops if i['ativo'] == item]
            compras = [i for i in ops_curr if i['tipo'] == 'C']
            vendas = [i for i in ops_curr if i['tipo'] == 'V']
            total_compras = sum([i['qtd'] for i in compras])
            total_vendas = sum([i['qtd'] for i in vendas])
            if total_vendas == total_compras:
                for op in ops_curr:
                    op['daytrade'] = True
            elif (total_vendas == 0 and total_compras != 0) or (total_vendas != 0 and total_compras == 0):
                for op in compras:
                    op['daytrade'] = False
            elif total_vendas != 0 and total_compras != 0 and len(vendas) + len(compras) > 3:
                for vd in vendas:
                    qtd = vd['qtd']
                    cps = [i for i in compras if i['qtd'] == qtd and i['daytrade'] is None]
                    if cps:
                        cps[0]['daytrade'] = True
                        vd['daytrade'] = True

                ops = [i for i in ops_curr if i['daytrade'] is None]
                if ops:
                    compras = [i for i in ops if i['tipo'] == 'C' and i['qtd'] % 100 == 0]
                    vendas = [i for i in ops if i['tipo'] == 'V' and i['qtd'] % 100 == 0]
                    total_compras = sum([i['qtd'] for i in compras])
                    total_vendas = sum([i['qtd'] for i in vendas])
                    if total_vendas == total_compras:
                        for op in compras + vendas:
                            op['daytrade'] = True

        # nada a fazer
        ops = [i for i in operacoes if i['daytrade'] is None]
        if ops:
            for op in ops:
                op['daytrade'] = False

        return sorted(operacoes, key=lambda x: x['daytrade'], reverse=True)

    @staticmethod
    def __new_operacao(item: Dict, nota: NotaCorretagem) -> Operacao:
        operacao = Operacao()
        if item['tipo'] == 'C':
            operacao.qtd_compra = item['qtd']
            operacao.pm_compra = item['preco']
            operacao.data_compra = nota.data_referencia
            operacao.nota_compra = nota
        elif item['tipo'] == 'V':
            operacao.qtd_venda = item['qtd']
            operacao.pm_venda = item['preco']
            operacao.data_venda = nota.data_referencia
            operacao.nota_venda = nota

        operacao.daytrade = item['daytrade']
        operacao.compra_venda = CompraVenda(item['tipo'])
        operacao.custos = item['custos']
        operacao.irpf = item['irpf']
        return operacao

    @staticmethod
    def __copy_operacao(old: Operacao) -> Operacao:
        operacao = Operacao()
        operacao.qtd_compra = old.qtd_compra
        operacao.qtd_venda = old.qtd_venda
        operacao.pm_compra = old.pm_compra
        operacao.pm_venda = old.pm_venda
        operacao.data_compra = old.data_compra
        operacao.data_venda = old.data_venda
        operacao.compra_venda = old.compra_venda
        operacao.custos = old.custos
        operacao.irpf = old.irpf
        operacao.nota_venda = old.nota_venda
        operacao.nota_compra = old.nota_compra
        operacao.ativo = old.ativo
        return operacao

    @classmethod
    def read_by_params(cls):
        input_schema = {
            'id': fields.Int(),
            'encerrada': fields.Bool(),
            'data_encerramento': fields.Date(),
            'groupby': fields.String(validate=[validate_group_by_operacoes])
        }
        args = parser.parse(input_schema, request, location='querystring')
        data = Operacao().read_by_params(args)
        response = rows_to_dicts(data)
        return response
