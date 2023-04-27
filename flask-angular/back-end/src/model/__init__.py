"""
 @author Marildo Cesar 22/04/2023
"""
from .sqllite_connection import SqlLiteConnection

from .tables import Operacoes, Carteira, Ativo, Setor, SubSetor, Segmento
from .enums import TipoInvestimento

from .init_db import create_base
create_base()
