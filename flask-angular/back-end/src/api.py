"""
 @author Marildo Cesar 03/05/2023
"""
from flask import Flask

from src.app import ConfigApp
from src.settings import config

flask_app = Flask(__name__)
ConfigApp(flask_app)

if __name__ == '__main__':
    @flask_app.before_request
    def before_request():
        pass


    @flask_app.after_request
    def set_response_headers(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response


    flask_app.run(port=config.get_api_port(), debug=config.get_api_debug(), host='0.0.0.0')
