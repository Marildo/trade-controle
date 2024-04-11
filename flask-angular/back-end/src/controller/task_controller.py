# @author Marildo Cesar 07/04/2024

import threading

from datetime import date

from ..model import Ativo, Indicadores, HistoricoAtivos
from ..services import ADVFNService, YFinanceService, InvestingService
from .wind_calculations import get_wind_fut


class TaskController:

    @classmethod
    def update_winfut(cls):
        def task():

            today = date.today()

            code, _ = get_wind_fut(today)
            wind = InvestingService.get_winfut_values()

            win_hist = HistoricoAtivos()
            WIN_ID = 800000
            win_hist.ativo_id = WIN_ID
            win_hist.fechamento = wind['close']
            win_hist.abertura = wind['open']
            win_hist.maxima = wind['high']
            win_hist.minima = wind['low']
            win_hist.data = wind['date'].date()
            win_hist.update()

            ativo = Ativo().read_by_id(WIN_ID)
            ativo.cotacao = wind['current']
            ativo.variacao = wind['day_variation']
            ativo.fechamento = wind['close']
            ativo.minima = wind['low']
            ativo.maxima = wind['high']
            ativo.abertura = wind['open']
            ativo.update()

            Indicadores.update_values({
                'win_code': code,
                'win_var': wind['day_variation'],
                'win_current': wind['current']
            })

        thread = threading.Thread(target=task)
        thread.start()

    @classmethod
    def update_ibove(cls):
        def task():
            advfn = ADVFNService()
            ibove = advfn.get_ibove_current()

            Indicadores.update_values({
                'ibove_var': ibove['day_variation'],
                'ibove_current': ibove['current']
            })

        thread = threading.Thread(target=task)
        thread.start()

    @classmethod
    def update_sp500fut(cls):
        def task():
            sp = InvestingService.get_sp500fut_values()
            Indicadores.update_values({
                'sp500fut_var': sp['day_variation'],
                'sp500fut_current': sp['current']
            })

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
            Indicadores.update_values(di)

        thread = threading.Thread(target=task)
        thread.start()
