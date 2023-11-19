# @author Marildo Cesar 19/09/2023
from typing import NamedTuple
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from ..services.fiis import load_dividendos
from ..services.status_invest import StatusInvest
from ..model import DividendosRepository, Dividendos
from .schemas import DividendosSchema
from .carteira_controller import CarteiraController


class DayHistoric(NamedTuple):
    data: date
    qtd: float


class DividendosController:

    @classmethod
    def summary(cls):
        today = date.today()
        dividendos = Dividendos.all()
        year = sum([i.total for i in dividendos if i.data_pgto.year == today.year])
        month = sum([i.total for i in dividendos if i.data_pgto >= today.replace(day=1)])
        total = sum([i.total for i in dividendos])
        data = DividendosSchema().dump(dividendos, many=True)
        return dict(year=year, month=month, total=total, items=data)

    @staticmethod
    def proccess():
        def new_dividendo():
            nd = Dividendos()
            nd.data_ref = data_ref
            nd.ativo_id = row.ativo_id
            nd.carteira_id = row.carteira_id
            nd.div_yield = 0
            return nd

        rows = DividendosRepository.load_ativos()
        for row in rows:
            diff = (row.dt_end - row.dt_start).days
            if diff < 30:
                continue
            dividendos = []
            payments = []
            month = row.dt_start.replace(day=1)
            end = date.today().replace(day=1) - relativedelta(months=1)
            while month < end:
                month += relativedelta(months=1)
                month -= timedelta(days=1)

                if not dividendos:
                    dividendos = Dividendos.find_by_ativo(row.ativo_id)

                data_ref = month.replace(day=1)
                exists = [i for i in dividendos if i.data_ref == data_ref]
                if exists:
                    continue

                print(f'Processing {row.codigo} - {month}')

                if not payments:
                    payments = load_dividendos(row.codigo) if row.tipo_investimento == 'FIIS' \
                        else StatusInvest().load_dividendos(row.codigo)

                pays = [i for i in payments if
                        i['data_com'].year == data_ref.year and i['data_com'].month == data_ref.month]
                if not pays:
                    div = new_dividendo()
                    div.data_com = month
                    div.qtd = DividendosRepository.get_qtd(row.ativo_id, div.data_com)
                    div.data_pgto = month
                    div.valor = 0
                    div.total = 0
                    div.ir = 0
                    div.save()
                else:
                    for pay in pays:
                        div = new_dividendo()
                        div.data_com = pay['data_com']
                        div.data_pgto = pay['data_pgto']
                        div.valor = pay['valor']
                        div.div_yield = pay['div_yield']
                        div.cotacao = pay['cotacao']
                        div.jcp = pay['jcp']
                        div.qtd = DividendosRepository.get_qtd(row.ativo_id, div.data_com)
                        total = div.qtd * div.valor
                        div.ir = total * (15 / 100) if div.jcp else 0
                        div.total = total - div.ir
                        div.save()
                        CarteiraController.update_by_dividendos(div, row.codigo)
                        CarteiraController.update_saldos()
