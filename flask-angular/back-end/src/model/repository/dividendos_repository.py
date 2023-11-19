# @author Marildo Cesar 19/09/2023
from sqlalchemy import text

from .. import db_connection
from ..scripts import DividendosSql


class DividendosRepository:

    @staticmethod
    def load_ativos():
        sql = text(DividendosSql.load_ativos)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql)
            return query.fetchall()

    @staticmethod
    def get_qtd(ativo_id: int, data_ref) -> float:
        sql = text(DividendosSql.get_qtd)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql, dict(ativo_id=ativo_id, data_ref=data_ref))
            return query.one().qtd
