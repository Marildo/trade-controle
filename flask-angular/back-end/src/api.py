"""
 @author Marildo Cesar 03/05/2023
"""
from src.api import App
from src.settings import config

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
