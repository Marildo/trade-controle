# @author Marildo Cesar 17/10/2023
from sqlalchemy import text, desc

from .. import db_connection
from .. import Carteira, Movimentacao, Historico
from ..scripts import CarteiraSQL


class CarteiraRepository:

    @classmethod
    def get_carteiras(cls):
        data = Carteira().read_by_params({})
        return data

    @classmethod
    def totalize(cls):
        with db_connection.engine.begin() as conn:
            sql = text(CarteiraSQL.totalize_saldo_ativos)
            conn.execute(sql)
            sql = text(CarteiraSQL.totalize_saldo_caixa)
            conn.execute(sql)
            sql = text(CarteiraSQL.totalize_resultado)
            conn.execute(sql)

    @classmethod
    def get_movimentacoes(cls, params: dict):
        filters = (
            Movimentacao.data_referencia >= params['start_date'],
            Movimentacao.data_referencia <= params['end_date']
        )
        with db_connection as conn:
            query = (conn.session.query(Movimentacao)
                     .filter(*filters)
                     .order_by(desc(Movimentacao.data_referencia))
                     )
            data = query.all()

        return data

    @classmethod
    def delete_movimentacao(cls, id_mov):
        with db_connection as conn:
            hist = conn.session.query(Historico).filter(Historico.movimento_id == id_mov).first()
            if hist:
                conn.session.delete(hist)
            item = conn.session.query(Movimentacao).filter(Movimentacao.id == id_mov).first()
            if item:
                conn.session.delete(item)

    @classmethod
    def get_historicos(cls):
        with db_connection.engine.begin() as conn:
            sql = text(CarteiraSQL.historico_sumarizado)
            query = conn.execute(sql)
        return query.all()
