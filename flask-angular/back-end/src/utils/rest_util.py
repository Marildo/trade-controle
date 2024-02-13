# @author Marildo Cesar 12/02/2024

from flask import request


def get_location(_request: request) -> str:
    _map = {
        'multipart/form-data': 'form',
        'application/json': 'json'
    }
    content_type = str(request.headers['Content-Type']).split(";")[0]
    return _map[content_type] if content_type in _map else 'querystring'
