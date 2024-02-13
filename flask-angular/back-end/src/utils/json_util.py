# @author Marildo Cesar 11/02/2024

import json

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        return str(obj)
