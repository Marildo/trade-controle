"""
 @author Marildo Cesar 03/05/2023
"""
from datetime import datetime

from flask import Blueprint
from .rest_response import format_response

name = 'IndexRouter'
resource = '/'
index_router = Blueprint(name=name, import_name=name, url_prefix=resource)


@index_router.route('', methods=['GET'])
@format_response
def index():
    response = {"Data": datetime.today()}
    return response
