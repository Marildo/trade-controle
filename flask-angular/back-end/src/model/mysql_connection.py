"""
 @author Marildo Cesar 27/05/2023
"""

from .connection import BaseConnection
from src.settings import config


class MysqlConnection(BaseConnection):

    def _get_url(self) -> str:
        user = config.load_value('DATABASE_USER')
        password = config.load_value('DATABASE_PASSWORD')
        port = config.load_value('DATABASE_PORT')
        host = config.load_value('DATABASE_HOST')
        database = config.load_value('DATABASE_NAME')
        charset = config.load_value('DATABASE_CHARSET')
        autocommit = False
        url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}&autocommit={autocommit}'
        return url
