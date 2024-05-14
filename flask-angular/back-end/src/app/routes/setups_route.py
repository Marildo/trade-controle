# @author Marildo Cesar 14/02/2024
from flask import Blueprint, request

from ...controller import BacktestController
from ...controller import SetupController

from .rest_response import format_response

name = 'SetupRouter'
resource = '/setups'
setups_router = Blueprint(name=name, import_name=name, url_prefix=resource)


@setups_router.route('', methods=['GET'])
@format_response
def summary():
    return SetupController.load(request)


@setups_router.route('', methods=['POST'])
@format_response
def process():
    return SetupController.save(request)


@setups_router.route('/calcs/daly', methods=['GET'])
@format_response
def ind_fut():
    return SetupController.daily_calcs(request)


@setups_router.route('/backtest', methods=['POST'])
@format_response
def backtest():
    return BacktestController.run(False)


@setups_router.route('/backtest/csv', methods=['POST'])
@format_response
def backtest_csv():
    return BacktestController.run(True)
