"""
 @author Marildo Cesar 24/04/2023
"""
import os
import logging

from dotenv import load_dotenv


class Settings():
    def __init__(self):
        load_dotenv()
        logging.basicConfig(format='%(asctime)s - %(message)s', level=self.get_level_log())

    def get_level_log(self) -> str:
        return self.load_value('LEVEL_LOG', 'INFO')

    def load_value(self, name, default=None):
        value = os.environ[name] if name in os.environ else default
        return value


config = Settings()
