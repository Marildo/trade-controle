"""
 @author Marildo Cesar 03/05/2023
"""

from flask_cors import CORS

from .routes import index_router, nota_router, operacao_router, dividendo_router, carteira_router
from .tasks import Tasks


class ConfigApp:
    def __init__(self, app):
        self.__app = app
        self.__config_cors()
        self.__register_routes()
        Tasks().start()

    def __register_routes(self):
        self.__app.register_blueprint(index_router)
        self.__app.register_blueprint(nota_router)
        self.__app.register_blueprint(operacao_router)
        self.__app.register_blueprint(dividendo_router)
        self.__app.register_blueprint(carteira_router)

    def __config_cors(self):
        CORS(self.__app,
             resources={
                 r"*": {
                     "origins": "*"
                 }
             })
