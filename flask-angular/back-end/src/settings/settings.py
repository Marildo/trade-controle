"""
 @author Marildo Cesar 24/04/2023
"""
import os

from dotenv import load_dotenv


class Settings:
    def __init__(self):
        load_dotenv()

    def get_level_log(self) -> str:
        return self.load_value('LEVEL_LOG', 'INFO')

    def load_value(self, name, default=None):
        value = os.environ[name] if name in os.environ else default
        return value

    def get_api_port(self) -> str:
        return self.load_value('API_PORT', '8000')

    def get_api_debug(self) -> str:
        return self.load_value('API_DEBUG', 0) == 1

    def get_path_notas(self) -> str:
        path = self.load_value('PATH_NOTAS', '../notas_pdf/')
        os.makedirs(path, exist_ok=True)
        return path


config = Settings()
