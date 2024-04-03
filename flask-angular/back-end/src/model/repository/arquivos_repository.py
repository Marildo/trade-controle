# @author Marildo Cesar 19/09/2023
from sqlalchemy import text

from .. import db_connection
from ..scripts import DividendosSql, ArquivosCorretagemSQL


class ArquivosRepository:

    @staticmethod
    def delete_operacoes_from_file_id(file_id: int):
        sql = text(ArquivosCorretagemSQL.get_operacoes_for_delete_by_file_id)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql, {'file_id': file_id})
            data = query.fetchall()

        sql_delete = text(ArquivosCorretagemSQL.delete_operacoes)
        for row in data:
            with db_connection.engine.begin() as conn:
                params = row._mapping
                query = conn.execute(sql_delete, params)
                print(query)

    @staticmethod
    def get_qtd(ativo_id: int, data_ref) -> float:
        sql = text(DividendosSql.get_qtd)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql, dict(ativo_id=ativo_id, data_ref=data_ref))
            return query.one().qtd
