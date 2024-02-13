"""
 @author Marildo Cesar 03/05/2023
"""

from flask_cors import CORS

from .routes import index_router, nota_router, operacao_router, dividendo_router, carteira_router, ativos_router
from .tasks import Tasks


class ConfigApp:
    def __init__(self, app):
        self.__config_cors(app)
        self.__register_routes(app)
        self.__register_events(app)
        Tasks().start()

    @staticmethod
    def __register_routes(app):
        app.register_blueprint(ativos_router)
        app.register_blueprint(index_router)
        app.register_blueprint(nota_router)
        app.register_blueprint(operacao_router)
        app.register_blueprint(dividendo_router)
        app.register_blueprint(carteira_router)

    @staticmethod
    def __config_cors(app):
        CORS(app,
             resources={
                 r"*": {
                     "origins": "*"
                 }
             })

    @staticmethod
    def __register_events(app):
        @app.after_request
        def set_response_headers(response):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response

        @app.before_request
        def before_request():
            pass
