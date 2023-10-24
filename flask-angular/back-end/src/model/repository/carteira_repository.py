# @author Marildo Cesar 17/10/2023
from sqlalchemy import text

from .. import db_connection
from .. import Carteira
from ..scripts import CarteiraSQL


class CarteiraRepository:

    @classmethod
    def get_carteiras(cls):
        data = Carteira().read_by_params({})
        return data

    @classmethod
    def totalize_saldo_caixa(cls):
        sql = text(CarteiraSQL.totalize_saldo_caixa)
        with db_connection.engine.begin() as conn:
            conn.execute(sql)

    @classmethod
    def totalize_saldo_ativos(cls):
        sql = text(CarteiraSQL.totalize_saldo_caixa)
        with db_connection.engine.begin() as conn:
            conn.execute(sql)