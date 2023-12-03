# @author Marildo Cesar 24/10/2023
from apscheduler.schedulers.background import BackgroundScheduler

from src.controller import OperacaoController, CarteiraController
from ..settings import logger

class Tasks:

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(func=self.__tasks, trigger="interval", minutes=30)

    def start(self):
        self.__tasks()
        self.scheduler.start()

    @classmethod
    def __tasks(cls):
        logger.info("Starting tasks")
        OperacaoController().update_historico()
        OperacaoController().update_prices()
        CarteiraController.update_saldos()
        CarteiraController.generate_historico()
