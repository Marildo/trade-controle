# @author Marildo Cesar 14/02/2024

from datetime import date, timedelta

from webargs.flaskparser import parser
from marshmallow import fields

from src.services import ADVFNService
from src.utils.number_util import marred_five
from src.utils.date_util import uteis_days
from ..model import Setup, Ativo
from .schemas import SetupSchema


class SetupController:

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
        code, expiration = cls.__get_wind_fut(date.today())
        winfut_values = advfn.get_winfut_values(code)
        data['win'] = winfut_values
        data['win']['code'] = code
        data['win']['expiration'] = str(expiration)
        data['win']['expiration_days'] = uteis_days(date.today(), expiration, holidays)

        ibove = Ativo().read_by_id(810000)
        data['IBOVE'] = {}
        data['IBOVE']['close'] = ibove.cotacao
        data['IBOVE']['high'] = ibove.maxima
        data['IBOVE']['low'] = ibove.minima
        data['IBOVE']['day_variation'] = advfn.get_ibove_variation()

        sp500futfut = Ativo().read_by_id(910000)
        data['SP500FUT'] = {}
        data['SP500FUT']['close'] = sp500futfut.cotacao
        data['SP500FUT']['high'] = sp500futfut.maxima
        data['SP500FUT']['low'] = sp500futfut.minima
        data['SP500FUT']['day_variation'] = advfn.get_sp500fut_variation()

        data['DI'] = advfn.get_di()

        # data['win']['close'] = 128805
        # data['SP500']['current_variation'] = 0.005700
        # data['SP500']['close'] = 4928.5
        # data['SP500']['high'] = 4960
        # data['SP500']['low'] = 4950
        # data['DI'] = 10.01
        # data['expiration_days'] = 8
        # data['IBOVE']['close'] = 128481.02

        data['win']['expectation'] = cls.__calc_win_price_expectation(data)

        return data

    @staticmethod
    def __get_wind_fut(reference_date: date):
        codes = {
            1: 'G', 2: 'G',
            3: 'J', 4: 'J',
            5: 'M', 6: 'M',
            7: 'Q', 8: 'Q',
            9: 'V', 10: 'V',
            11: 'Z', 12: 'Z',
        }

        expirations_date = {
            'G': 2,
            'J': 4,
            'M': 6,
            'Q': 8,
            'V': 10,
            'Z': 12
        }

        month = reference_date.month
        expiration_code = codes[month]
        code = f'WIN{expiration_code}{reference_date.strftime("%y")}'

        expr = date(day=15, month=expirations_date[expiration_code], year=reference_date.year)
        WEDNESDAY = 3
        days_off_wed = (expr.weekday() - WEDNESDAY) % 7
        expiration = expr + timedelta(days=days_off_wed - 1)
        return code, expiration

    @staticmethod
    def __calc_win_price_expectation(data: dict):
        EULER = 2.71828
        DIAS_UTEIS_BRASIL = 252

        win = data['win']
        lclose = win['close']

        sp500fut = data['SP500FUT']
        var_sp500fut = sp500fut['day_variation'] * 0.01

        open = marred_five(lclose * var_sp500fut + lclose)
        high = marred_five(sp500fut['high'] / sp500fut['close'] * open)
        low = marred_five(sp500fut['low'] / sp500fut['close'] * open)

        dividendos_anuais = 3.795 * 0.01
        di = data['DI']['value'] * 0.01

        fee_by_time = win['expiration_days'] * 1 / DIAS_UTEIS_BRASIL
        fee = (di - dividendos_anuais) * fee_by_time
        fair = marred_five(data['IBOVE']['close'] * EULER ** fee)

        return {'open': open, 'high': high, 'low': low, 'fair': fair}
