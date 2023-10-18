# @author Marildo Cesar 17/10/2023


from .. import db_connection
from .. import Carteira


class CarteiraRepository:

    @classmethod
    def get_carteiras(cls):
        data = Carteira().read_by_params({})
        return data
