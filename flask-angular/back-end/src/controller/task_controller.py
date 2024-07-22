# @author Marildo Cesar 07/04/2024

import threading

from datetime import date, datetime, time

from ..model import Ativo, Indicadores, HistoricoAtivos
from ..model.simple_connection import SimpleConnection
from ..services import ADVFNService, YFinanceService, InvestingService, BCBService
from .calculations import get_wind_fut


class TaskController:

    @classmethod
    def update_winfut(cls):
        def task():
            today = date.today()

            code, _ = get_wind_fut(today)
            wind = InvestingService.get_winfut_values()

            WIN_ID = 800000

            values = {}
            values['fechamento'] = wind['close']
            values['abertura'] = wind['open']
            values['maxima'] = wind['high']
            values['minima'] = wind['low']
            values['update_at'] = datetime.now()

            keys = {}
            keys['ativo_id'] = WIN_ID
            keys['data'] = wind['date'].date()

            with SimpleConnection() as conn:
                rs = conn.update('historico_ativos', values, keys)
                if rs == 0:
                    win_hist = HistoricoAtivos()
                    WIN_ID = 800000
                    win_hist.ativo_id = WIN_ID
                    win_hist.fechamento = wind['close']
                    win_hist.abertura = wind['open']
                    win_hist.maxima = wind['high']
                    win_hist.minima = wind['low']
                    win_hist.data = keys['data']
                    win_hist.update()

            with SimpleConnection() as conn:
                values = {'cotacao': wind['current'],
                          'variacao': wind['day_variation'],
                          'fechamento': wind['close'],
                          'minima': wind['low'],
                          'maxima': wind['high'],
                          'abertura': wind['open'],
                          'update_at': datetime.now()}
                conn.update('ativos', values, {'id': WIN_ID})

            with SimpleConnection() as conn:
                values = {
                    'win_code': code,
                    'win_var': wind['day_variation'],
                    'win_current': wind['current'],
                    'update_at': datetime.now()
                }
                conn.update('indicadores', values, {'1': 1})

        thread = threading.Thread(target=task)
        thread.start()

    @classmethod
    def update_dx(cls):
        def task():
            dx = InvestingService.get_dx_values()
            DX_ID = 950000
            values = {
                'fechamento': dx['close'],
                'abertura': dx['open'],
                'maxima': dx['high'],
                'minima': dx['low'],
                'update_at': datetime.now()
            }

            with SimpleConnection() as conn:
                keys = {'ativo_id': DX_ID, 'data': dx['date']}
                rs = conn.update('historico_ativos', values, keys)
                if rs == 0:
                    dx_hist = HistoricoAtivos()
                    dx_hist.ativo_id = DX_ID
                    dx_hist.fechamento = dx['close']
                    dx_hist.abertura = dx['open']
                    dx_hist.maxima = dx['high']
                    dx_hist.minima = dx['low']
                    dx_hist.data = dx['date']
                    dx_hist.update()

            with SimpleConnection() as conn:
                values['cotacao'] = dx['current']
                values['variacao'] = dx['day_variation']
                keys = {'id': DX_ID}
                conn.update('ativos', values, keys)

            with SimpleConnection() as conn:
                values = {
                    'dx_var': dx['day_variation'],
                    'dx_current': dx['current'],
                    'update_at': datetime.now()
                }
                conn.update('indicadores', values, {'1': 1})

        thread = threading.Thread(target=task)
        thread.start()

    @classmethod
    def update_ibove(cls):
        def task():
            advfn = ADVFNService()
            ibove = advfn.get_ibove_current()
            if ibove:
                with SimpleConnection() as conn:
                    values = {
                        'ibove_var': ibove['day_variation'],
                        'ibove_current': ibove['current'],
                        'update_at': datetime.now()
                    }
                    conn.update('indicadores', values, {'1': 1})

        thread = threading.Thread(target=task)
        thread.start()

    @classmethod
    def update_sp500fut(cls):
        def task():
            sp = InvestingService.get_sp500fut_values()
            with SimpleConnection() as conn:
                values = {
                    'sp500fut_var': sp['day_variation'],
                    'sp500fut_current': sp['current'],
                    'update_at': datetime.now()
                }
                conn.update('indicadores', values, {'1': 1})

        thread = threading.Thread(target=task)
        thread.start()

    @classmethod
    def update_indices(cls):
        ativos = Ativo.find_like_name('INDICE')
        for a in ativos:
            YFinanceService.update_indices(a)

    def update_di(self):
        def task():
            advfn = ADVFNService()
            di = advfn.get_di()
            with SimpleConnection() as conn:
                conn.update('indicadores', di, {'1': 1})

        thread = threading.Thread(target=task)
        thread.start()

    def update_usb_brl_fut(self):
        def task():
            DOL_ID = 900000
            data = InvestingService.get_usd_brl_fut_values()

            with SimpleConnection() as conn:
                values = {
                    'fechamento': data['close'],
                    'abertura': data['open'],
                    'maxima': data['high'],
                    'minima': data['low'],
                    'update_at': datetime.now()
                }
                keys = {'ativo_id': DOL_ID, 'data': data['date']}
                rs = conn.update('historico_ativos', values, keys)
                if rs == 0:
                    dx_hist = HistoricoAtivos()
                    dx_hist.ativo_id = DOL_ID
                    dx_hist.fechamento = data['close']
                    dx_hist.abertura = data['open']
                    dx_hist.maxima = data['high']
                    dx_hist.minima = data['low']
                    dx_hist.data = data['date']
                    dx_hist.update()

            with SimpleConnection() as conn:
                values = {'cotacao': data['current'],
                          'variacao': data['day_variation'],
                          'fechamento': data['close'],
                          'minima': data['low'],
                          'maxima': data['high'],
                          'abertura': data['open'],
                          'update_at': datetime.now()}
                conn.update('ativos', values, {'id': DOL_ID})

            with SimpleConnection() as conn:
                values = {
                    'usdbrl_var': data['day_variation'],
                    'usdbrl_current': data['current'],
                    'update_at': datetime.now()
                }
                conn.update('indicadores', values, {'1': 1})

        thread = threading.Thread(target=task)
        thread.start()

    def update_usb_brl(self):
        def task():
            DOL_ID = 905000
            data = InvestingService.get_usd_brl_values()

            with SimpleConnection() as conn:
                values = {
                    'fechamento': data['close'],
                    'abertura': data['open'],
                    'maxima': data['high'],
                    'minima': data['low'],
                    'update_at': datetime.now()
                }
                ref_date = data['date'].date()
                keys = {'ativo_id': DOL_ID, 'data': ref_date}
                rs = conn.update('historico_ativos', values, keys)
                if rs == 0:
                    dx_hist = HistoricoAtivos()
                    dx_hist.ativo_id = DOL_ID
                    dx_hist.fechamento = data['close']
                    dx_hist.abertura = data['open']
                    dx_hist.maxima = data['high']
                    dx_hist.minima = data['low']
                    dx_hist.data = ref_date
                    dx_hist.update()

            with SimpleConnection() as conn:
                values = {'cotacao': data['current'],
                          'variacao': data['day_variation'],
                          'fechamento': data['close'],
                          'minima': data['low'],
                          'maxima': data['high'],
                          'abertura': data['open'],
                          'update_at': datetime.now()}
                conn.update('ativos', values, {'id': DOL_ID})

        thread = threading.Thread(target=task)
        thread.start()

    def update_ptax(self):
        def task():
            ptax = BCBService().get_last_ptax()
            if ptax:
                with SimpleConnection() as conn:
                    conn.update('indicadores', {'ptax': ptax}, {'1': 1})

        today = datetime.today()
        if today.time() > time(hour=16, minute=10) or today.isoweekday() in (6, 7):
            return

        thread = threading.Thread(target=task)
        thread.start()
