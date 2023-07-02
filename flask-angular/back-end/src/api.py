"""
 @author Marildo Cesar 03/05/2023
"""
import threading
import time

from src.api import App
from src.settings import config
from src.controller import AtivoController


def update_ativos():
    while True:
        AtivoController.update_prices()
        t_sleep = 60 * 60
        time.sleep(t_sleep)


t = threading.Thread(target=update_ativos)
t.start()

if __name__ == '__main__':
    retaguarda_app = App()
    app = retaguarda_app.get_app()


    @app.before_request
    def before_request():
        pass


    @app.after_request
    def set_response_headers(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response


    app.run(port=config.get_api_port(), debug=config.get_api_debug())
