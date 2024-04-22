# @author Marildo Cesar 06/04/2024
import math
from datetime import date, timedelta

from ..utils.number_util import marred_five


def get_wind_fut(reference_date: date):
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
    expiration = expr + timedelta(days=days_off_wed - 2)
    return code, expiration


def calc_win_price_expectation(data: dict):
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
    FPAC = marred_five(data['IBOVE']['close'] * EULER ** fee)  # fair price at closing
    FPC = marred_five(data['IBOVE']['current'] * EULER ** fee)

    return {'open': open, 'high': high, 'low': low, 'FPAC': FPAC, 'FPC': FPC}


def calc_volatiliadade(historicos, current_value_win):
    historicos = sorted(historicos, key=lambda x: x.data)
    data = []
    for i in historicos:
        data.append(i.as_dict())

    total_rd = 0
    total_rd2 = 0
    total_close = data[0]['fechamento']
    for i in range(1, len(data)):
        pr_relativo = data[i]['fechamento'] / data[i - 1]['fechamento']
        data[i]['retorno_diario'] = math.log(pr_relativo)
        data[i]['retorno_diario_2'] = math.log(pr_relativo) ** 2
        data[i]['preco_relativo'] = pr_relativo
        total_rd += data[i]['retorno_diario']
        total_rd2 += data[i]['retorno_diario_2']
        total_close += data[i]['fechamento']

    last_close = data[-1]['fechamento']
    total_rd2_per_regs = total_rd2 / 119
    total_rd_pot_twq = total_rd ** 2
    fator_reg = 120 * 119  # (len(data) - 1) * len(data)
    total_rd_pot_twq_per_fat = total_rd_pot_twq / fator_reg
    parc = total_rd2_per_regs - total_rd_pot_twq_per_fat
    volatilidade = math.sqrt(parc) * 100
    _avg = total_close / len(data)
    avg_perct = total_rd / (len(data) - 1) * 100

    anchors = {
        (3.99, 'p01', '0.0001%'),
        (2.58, 'p05', '0.05%'),
        (1.64, 'p5', '5%'),
        (1.28, 'p10', '10%'),
        (0.84, 'p20', '20%'),
        (0.53, 'p30', '30%'),
        (0.25, 'p40', '40%')
    }

    result = [
        {'percent': '50%', 'value': last_close, 'class': 'p50'},
        {'percent': 'Atual', 'value': current_value_win, 'class': 'atual'}
    ]
    for v, c, p in anchors:
        calc = (v * volatilidade) + avg_perct
        value = (last_close * calc) * 0.01
        value = marred_five(last_close + value)
        result.append({'percent': p, 'value': value, 'class': c})

        calc = (-1 * v * volatilidade) + avg_perct
        value = (last_close * calc) * 0.01
        value = marred_five(last_close + value)
        result.append({'percent': p, 'value': value, 'class': c})

    result = sorted(result, key=lambda d: d['value'], reverse=True)
    return result
