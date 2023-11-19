# @author Marildo Cesar 19/09/2023
from sqlalchemy import text

from .. import db_connection
from ..scripts import OperacoesSql


class OperacoesRepository:
    pass

    # TODO -  remover
    @classmethod
    def query_compras_without_historic(cls):
        sql = text(OperacoesSql.query_compras_without_historic)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql)
            return query.fetchall()

    # TODO -  remover
    @classmethod
    def query_vendas_without_historic(cls):
        sql = text(OperacoesSql.query_vendas_without_historic)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql)
            return query.fetchall()
