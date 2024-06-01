# @author Marildo Cesar 19/09/2023
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from .. import db_connection
from ..scripts import DividendosSql, ArquivosCorretagemSQL


class ArquivosRepository:

    @staticmethod
    def delete_operacoes_from_file_id(file_id: int):
        sql = text(ArquivosCorretagemSQL.get_operacoes_for_delete_by_file_id)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql, {'file_id': file_id})
            data = query.fetchall()

        sqls = ArquivosCorretagemSQL.delete_operacoes.split(";")
        sqls_delete = [i for i in sqls]
        with db_connection.engine.begin() as conn:
            for row in data:
                params = row._mapping
                for sql in sqls_delete:
                    try:
                        query = conn.execute(text(sql), params)
                        print(query.rowcount)
                    except IntegrityError:
                        pass

    @staticmethod
    def get_qtd(ativo_id: int, data_ref) -> float:
        sql = text(DividendosSql.get_qtd)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql, dict(ativo_id=ativo_id, data_ref=data_ref))
            return query.one().qtd
