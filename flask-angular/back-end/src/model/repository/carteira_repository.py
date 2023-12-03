# @author Marildo Cesar 17/10/2023
from sqlalchemy import text

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
    def get_movimentacoes(cls):
        data = Movimentacao().read_by_params({})
        return data

    @classmethod
    def get_historicos(cls):
        data = Historico().read_by_params({})
        return data
