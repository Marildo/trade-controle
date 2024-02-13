# @author Marildo Cesar 09/02/2024

from flask import Blueprint, request

from .rest_response import format_response

from ...controller import BacktestController

name = 'AtivosRouter'
resource = '/ativos'
ativos_router = Blueprint(name=name, import_name=name, url_prefix=resource)


@ativos_router.route('/backtest', methods=['POST'])
@format_response
def backtest():
    return BacktestController.run(False)


@ativos_router.route('/backtest/csv', methods=['POST'])
@format_response
def backtest_csv():
    return BacktestController.run(True)
