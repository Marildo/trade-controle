# @author Marildo Cesar 14/02/2024

from datetime import date, timedelta
import math

from webargs.flaskparser import parser
from marshmallow import fields

from src.services import ADVFNService
from src.utils.number_util import marred_five
from src.utils.date_util import uteis_days
from ..model import Setup, Ativo, HistoricoAtivos
from .schemas import SetupSchema
from .wind_calculations import get_wind_fut, calc_win_price_expectation, calc_volatiliadade


class SetupController:
    WIN_ID = 900000

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
        holidays = []  # TODO - Carregar da tabela
        data = {}

        advfn = ADVFNService()
        code, expiration = get_wind_fut(date.today())
        winfut_values = advfn.get_winfut_values(code)
        data['win'] = winfut_values
        wind = data['win']
        wind['code'] = code
        wind['expiration'] = str(expiration)
        wind['expiration_days'] = uteis_days(date.today(), expiration, holidays)

        win_hist = HistoricoAtivos()
        win_hist.ativo_id = cls.WIN_ID
        win_hist.abertura = wind['open']
        win_hist.fechamento = wind['close']
        win_hist.maxima = wind['high']
        win_hist.minima = wind['low']
        win_hist.data = wind['date']
        win_hist.save(update_on_duplicate=True)

        params = {
            'ativo_id': cls.WIN_ID,
            'orderBy': 'dataDESC',
            'LIMIT': 121
        }
        historicos = HistoricoAtivos().read_by_params(params)

        if wind['date'] == date.today():
            wind['open'] = historicos[1].abertura
            wind['close'] = historicos[1].fechamento
            wind['high'] = historicos[1].maxima
            wind['low'] = historicos[1].minima

        ibove = Ativo().read_by_id(810000)
        data['IBOVE'] = advfn.get_ibove_current()
        data['IBOVE']['close'] = ibove.cotacao
        data['IBOVE']['high'] = ibove.maxima
        data['IBOVE']['low'] = ibove.minima

        sp500futfut = Ativo().read_by_id(910000)
        data['SP500FUT'] = advfn.get_sp500fut_variation()
        data['SP500FUT']['close'] = sp500futfut.cotacao
        data['SP500FUT']['high'] = sp500futfut.maxima
        data['SP500FUT']['low'] = sp500futfut.minima

        data['DI'] = advfn.get_di()

        # data['win']['close'] = 128805
        # data['SP500']['current_variation'] = 0.005700
        # data['SP500']['close'] = 4928.5
        # data['SP500']['high'] = 4960
        # data['SP500']['low'] = 4950
        # data['DI'] = 10.01
        # data['expiration_days'] = 8
        # data['IBOVE']['close'] = 128481.02

        data['win']['expectation'] = calc_win_price_expectation(data)
        data['win']['volatility'] = calc_volatiliadade(historicos)

        return data
