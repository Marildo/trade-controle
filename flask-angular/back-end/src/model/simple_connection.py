# @author Marildo Cesar 01/05/2024

import pymysql
from typing import List, Dict
from src.settings import config


class SimpleConnection:
    def __init__(self):
        self.connection: pymysql.Connection

    def __enter__(self):
        user = config.load_value('DATABASE_USER')
        password = config.load_value('DATABASE_PASSWORD')
        port = int(config.load_value('DATABASE_PORT'))
        host = config.load_value('DATABASE_HOST')
        database = config.load_value('DATABASE_NAME')
        self.connection = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def query(self, sql: str) -> List:
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            fields = [i[0] for i in cursor.description]
            result = []
            for rs in data:
                row = {}
                for i in range(len(fields)):
                    row[fields[i]] = rs[i]
                result.append(row)
            return result
        finally:
            if cursor:
                cursor.close()

    def execute(self, sql, params: Dict):
        cursor = self.connection.cursor()
        try:
            rs = cursor.execute(sql, params)
            self.connection.commit()
            return rs
        except pymysql.Error as e:
            self.connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()

    def update(self, table: str, values: Dict, keys: Dict):
        cursor = self.connection.cursor()
        try:
            values_params = ', '.join([f"{k}='{v}'" for k, v in values.items()])
            key_params = ' AND '.join([f"{k}='{v}'" for k, v in keys.items()])
            SQL = f"UPDATE {table} SET {values_params} WHERE {key_params}"
            rs = cursor.execute(SQL)
            self.connection.commit()
            return rs
        except pymysql.Error as e:
            self.connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
