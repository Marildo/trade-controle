"""
 @author Marildo Cesar 30/05/2023
"""
from typing import List, Dict
from datetime import datetime, date

from sqlalchemy.engine.row import Row


def rows_to_dicts(query: List[Row]) -> List[Dict]:
    result = []
    for i in query:
        row = dict(i._mapping)
        for k, v in row.items():
            if isinstance(v, (date, datetime)):
                row[k] = str(v)

        result.append(row)

    return result
