"""
 @author Marildo Cesar 25/04/2023
"""

from sqlalchemy.ext.declarative import declarative_base
# from .sqllite_connection import SqlLiteConnection
from .mysql_connection import MysqlConnection

Base = declarative_base()
db_connection = MysqlConnection()


def create_base():
    Base.metadata.create_all(db_connection.engine)
