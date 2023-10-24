# @author Marildo Cesar 24/10/2023
from apscheduler.schedulers.background import BackgroundScheduler

from ..controller import OperacaoController, CarteiraController


class Tasks:

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(func=self.__tasks, trigger="interval", minutes=30)

    def start(self):
        self.__tasks()
        self.scheduler.start()

    @classmethod
    def __tasks(cls):
        OperacaoController().update_prices()
        CarteiraController.update_saldos()
