"""
 @author Marildo Cesar 22/04/2023
"""
from .init_db import db_connection
from .tables import Operacao, NotaCorretagem, Carteira, Ativo, Setor, SubSetor, Segmento
from .enums import TipoInvestimento, TipoNota, CompraVenda

from .init_db import create_base

create_base()
