# @author Marildo Cesar 19/09/2023
from typing import NamedTuple
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from src.services.status_invest import StatusInvest
from model import DividendosRepository, Dividendos
from .schemas import DividendosSchema


class DayHistoric(NamedTuple):
    data: date
    qtd: float


class DividendosController:

    @classmethod
    def summary(cls):
        today = date.today()
        dividendos = Dividendos.all()
        year = sum([i.total for i in dividendos if i.data_ref.year == today.year])
        month = sum([i.total for i in dividendos if i.data_ref >= today.replace(day=1)])
        total = sum([i.total for i in dividendos])
        data = DividendosSchema().dumps(dividendos, many=True)
        return dict(year=year, month=month, total=total, items=data)

    @staticmethod
    def proccess():
        statusI = StatusInvest()
        rows = DividendosRepository.load_ativos()
        for row in rows:
            dividendos = []
            payments = []
            month = row.start.replace(day=1)
            end = date.today().replace(day=1) - relativedelta(months=1)
            while month < end:
                month += relativedelta(months=1)
                month -= timedelta(days=1)

                if not dividendos:
                    dividendos = Dividendos.find_by_ativo(row.ativo_id)

                exists = [i for i in dividendos if i.data_ref == month]
                if exists:
                    continue

                qtd = DividendosRepository.get_qtd(row.ativo_id, month)

                if not payments:
                    payments = statusI.load_dividendos_fiis(row.codigo)

                div = Dividendos()
                div.data_ref = month
                div.ativo_id = row.ativo_id
                div.qtd = qtd

                pays = [i for i in payments if i['data_com'].year == month.year and i['data_com'].month == month.month]
                if pays:
                    div.data_com = pays[0]['data_com']
                    div.data_pgto = pays[0]['data_pgto']
                    div.valor = pays[0]['valor']
                else:
                    div.data_com = month
                    div.data_pgto = month
                    div.valor = 0

                div.data_ref = div.data_pgto.replace(day=1)
                div.total = div.qtd * div.valor
                div.save()
