# @author Marildo Cesar 14/02/2024

from datetime import date

from marshmallow import fields
from webargs.flaskparser import parser

from src.utils.date_util import uteis_days
from .schemas import SetupSchema
from .wind_calculations import get_wind_fut, calc_win_price_expectation, calc_volatiliadade
from ..model import Setup, Ativo, Indicadores, HistoricoAtivos, Feriados


class SetupController:
    WIN_ID = 800000

    @classmethod
    def load(cls, request):
        data = Setup().read_by_params({})
        result = SetupSchema().dump(data, many=True)
        return result

    @classmethod
    def save(cls, request):
        input_schema = {
            'nome': fields.Str(required=True),
            'descricao': fields.Str(required=True),
        }
        args = parser.parse(input_schema, request, location='json')
        setup = Setup(**args)
        setup.save()
        return SetupSchema().dump(setup)

    @classmethod
    def ind_fut(cls, request):
        holidays = Feriados.get(date.today().year)
        data = {}

        code, expiration = get_wind_fut(date.today())

        indicatores = Indicadores().read_by_id(1)

        wdo = Ativo().read_by_id(cls.WIN_ID)

        data['win'] = {
            'day_variation': indicatores.win_var,
            'current': indicatores.win_current,
            'open': wdo.abertura,
            'close': wdo.fechamento,
            'low': wdo.minima,
            'high': wdo.maxima,
        }

        wind = data['win']
        wind['code'] = code
        wind['expiration'] = str(expiration)
        wind['expiration_days'] = uteis_days(date.today(), expiration, holidays)

        ibove = Ativo().read_by_id(810000)
        data['IBOVE'] = {
            'day_variation': indicatores.ibove_var,
            'current': indicatores.ibove_current,
            'open': ibove.abertura,
            'close': ibove.fechamento,
            'low': ibove.minima,
            'high': ibove.maxima,
        }

        sp500fut = Ativo().read_by_id(910000)
        data['SP500FUT'] = {
            'day_variation': indicatores.sp500fut_var,
            'current': indicatores.sp500fut_current,
            'open': sp500fut.abertura,
            'close': sp500fut.fechamento,
            'low': sp500fut.minima,
            'high': sp500fut.maxima,
        }

        data['DI'] = {
            'code': indicatores.di_code,
            'value': indicatores.di_current
        }

        # data['win']['close'] = 128805
        # data['SP500']['current_variation'] = 0.005700
        # data['SP500']['close'] = 4928.5
        # data['SP500']['high'] = 4960
        # data['SP500']['low'] = 4950
        # data['DI'] = 10.01
        # data['expiration_days'] = 8
        # data['IBOVE']['close'] = 128481.02

        data['win']['expectation'] = calc_win_price_expectation(data)

        params = {
            'ativo_id': cls.WIN_ID,
            'orderBy': 'dataDESC',
            'LIMIT': 121
        }
        historicos = HistoricoAtivos().read_by_params(params)
        data['win']['volatility'] = calc_volatiliadade(historicos, wind['current'])

        return data
