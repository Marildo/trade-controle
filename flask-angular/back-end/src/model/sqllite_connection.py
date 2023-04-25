"""
 @author Marildo Cesar 24/04/2023
"""

from .connection import BaseConnection
from src.settings import config


class SqlLiteConnection(BaseConnection):

    def _get_url(self) -> str:
        database = config.load_value('DATABASE_NAME')
        url = f'sqlite:///{database}.db'
        return url
