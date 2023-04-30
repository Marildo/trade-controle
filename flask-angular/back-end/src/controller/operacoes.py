"""
 @author Marildo Cesar 25/04/2023
"""
from datetime import datetime
from json import dumps
from typing import Dict, List

from sqlalchemy.exc import SQLAlchemyError

from src.settings import logger
from src.model import db_connection, Operacao, NotaCorretagem, CompraVenda
from src.model.dtos import Nota

from .ativos import AtivoController


class OperacaoController:

    @classmethod
    def save_operacoes(cls, notas: List[Nota]):

        map_order = {
            'C': lambda x: x.data_venda,
            'V': lambda x: x.data_compra,
        }

        today = datetime.today()
        for item in notas:
            session = db_connection.session
            try:
                nota_corr = NotaCorretagem(comprovante=item.comprovante, data_referencia=item.data_operacao,
                                           tipo=item.tipo_nota, data_upload=today)
                # if nota_corr.is_exists():
                #     logger.warn(f'Nota já foi importada ({nota_corr})')
                #     return

                session.merge(nota_corr)
                session.flush()

                for op in item.operacoes:
                    tipo_operacao = op['tipo']
                    logger.info(f'Store: Nota: {nota_corr.comprovante} - op: {dumps(op)}')
                    ativo = AtivoController.find_by_or_save(op['ativo'])
                    c_v = CompraVenda.VENDA if tipo_operacao == 'C' else CompraVenda.COMPRA
                    operacoes = Operacao.find_not_closed(ativo, c_v)

                    if not operacoes:
                        operacao = cls.__new_operacao(op, nota_corr)
                        operacao.ativo = ativo
                        session.add(operacao)
                        session.flush()
                    else:
                        operacoes.sort(key=map_order[tipo_operacao])
                        computed = 0
                        while computed != op['qtd']:
                            for row in operacoes:
                                if tipo_operacao == 'V':
                                    computed += row.qtd_compra
                                    if row.qtd_compra <= op['qtd']:
                                        row.qtd_venda =  row.qtd_compra
                                        row.pm_venda = op['preco']
                                        row.custos = op['custos']
                                        row.irpf = op['irpf']
                                        row.nota_venda = nota_corr
                                        row.data_venda = nota_corr.data_referencia
                                        row.encerrada = True
                                        row.daytrade = row.data_compra == row.data_venda
                                        row.data_encerramento = today
                                    elif row.qtd_compra > op['qtd']:
                                        new_op = cls.__copy_operacao(row)
                                        new_op.qtd_venda = op['qtd']
                                        new_op.qtd_compra = op['qtd']
                                        new_op.pm_venda = op['preco']
                                        new_op.custos = op['custos']
                                        new_op.irpf = op['irpf']
                                        row.nota_venda = nota_corr
                                        new_op.data_venda = nota_corr.data_referencia
                                        new_op.encerrada = True
                                        new_op.data_encerramento = today
                                        row.qtd_compra -= op['qtd']
                                        session.add(new_op)
                                else:
                                    if row.qtd_venda <= op['qtd']:
                                        computed += row.qtd_venda
                                        row.qtd_compra = row.qtd_venda
                                        row.pm_compra = op['preco']
                                        row.custos = op['custos']
                                        row.irpf = op['irpf']
                                        row.data_compra = nota_corr.data_referencia
                                        row.nota_compra = nota_corr
                                        row.encerrada = True
                                        row.data_encerramento = today
                                        row.daytrade = row.data_compra == row.data_venda
                                    elif row.qtd_venda > op['qtd']:
                                        computed += op['qtd']
                                        new_op = cls.__copy_operacao(row)
                                        new_op.qtd_venda = op['qtd']
                                        new_op.qtd_compra = op['qtd']
                                        new_op.pm_compra = op['preco']
                                        new_op.custos = op['custos']
                                        new_op.irpf = op['irpf']
                                        new_op.data_compra = nota_corr.data_referencia
                                        new_op.nota_compra = nota_corr
                                        new_op.encerrada = True
                                        new_op.data_encerramento = today
                                        row.qtd_venda -= op['qtd']
                                        session.add(new_op)

                                session.add(row)
                                session.flush()

                            if computed > op['qtd']:
                                operacao = cls.__new_operacao(op, nota_corr)
                                operacao.ativo = ativo
                                if tipo_operacao == 'V':
                                    operacao.qtd_compra = op['qtd'] - computed
                                else:
                                    operacao.qtd_venda = op['qtd'] - computed
                                session.add(operacao)

                                computed = op['qtd']

                        session.commit()

            except SQLAlchemyError as ex:
                print(ex)
                raise ex

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
