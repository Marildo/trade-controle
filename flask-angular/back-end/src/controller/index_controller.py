"""
 @author Marildo Cesar 02/07/2023
"""

from src.controller import AtivoController


class IndexController:

    @classmethod
    def start_services(cls):
        response = dict(update_price=False)
        try:
            AtivoController.update_prices()
            response['update_price'] = True
        except Exception as ex:
            response['error'] = str(ex)

        return response
