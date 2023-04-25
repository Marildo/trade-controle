"""
 @author Marildo Cesar 22/04/2023
"""

from .tables import Base, Operacoes
from .sqllite_connection import SqlLiteConnection

db_connection = SqlLiteConnection()
Base.metadata.create_all(db_connection.engine)
