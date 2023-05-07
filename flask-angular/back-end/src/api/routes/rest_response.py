"""
 @author Marildo Cesar 06/05/2023
"""
import traceback
from collections import OrderedDict
from functools import wraps

from flask import make_response, jsonify
from werkzeug.exceptions import BadRequest, NotFound

from settings import logger

def format_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        content = OrderedDict()
        content['success'] = False
        data = None
        try:
            result = func(*args, **kwargs)
            if isinstance(result, tuple):
                data, status_code = result
            else:
                status_code = 200
                content['success'] = True
                data = result
        except (BadRequest, NotFound) as ex:
            status_code = ex.code
            data = {'error': __format_badrequest(ex)}
        except Exception as e:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            status_code = 500
            data = {'error': str(e)}

        if data:
            content['data'] = data
        response = make_response(jsonify(content), status_code)
        response.headers['Content-Type'] = 'application/json'
        return response

    return wrapper


def __format_badrequest(exception: BadRequest):
    result = dict(message=exception.description)
    return result
