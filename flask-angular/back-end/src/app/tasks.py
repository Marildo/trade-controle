# @author Marildo Cesar 24/10/2023

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from src.controller import OperacaoController, CarteiraController, TaskController
from ..settings import logger


class Tasks:

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(func=self.__tasks, trigger="interval", minutes=30)
        self.scheduler.add_job(func=self.__update_indicadores, trigger="interval", minutes=1)

    def start(self):
        self.__tasks()
        self.__update_indicadores()
        self.scheduler.start()

    @classmethod
    def __tasks(cls):
        logger.info("Starting tasks")
        OperacaoController().update_historico()
        OperacaoController().update_prices()
        TaskController().update_indices()
        CarteiraController.update_saldos()
        CarteiraController.generate_historico()

    @classmethod
    def __update_indicadores(cls):
        hour = datetime.today().hour
        minute = datetime.today().minute
        # if hour > 19 and minute not in (0, 30):
        #     return

        logger.info("Starting updates")
        TaskController().update_winfut()
        TaskController().update_ibove()
        TaskController().update_sp500fut()
        TaskController().update_di()
