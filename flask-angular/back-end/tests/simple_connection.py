# @author Marildo Cesar 01/05/2024

from src.model.simple_connection import SimpleConnection


def query():
    with SimpleConnection() as conn:
        rs = conn.query('SELECT * FROM ATIVOS')
        for i in rs:
            print(i)


def execute():
    with SimpleConnection() as conn:
        params = {'parent_id': 0}
        rs = conn.execute("UPDATE `invest_controll`.`ativos` SET `update_at`='2024-05-01 00:00:44' WHERE  parent_id=%(parent_id)s", params)


execute()
