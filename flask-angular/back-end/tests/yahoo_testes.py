# @author Marildo Cesar 02/11/2023
from datetime import date
from src.services.yfinances import YFinanceService

test = YFinanceService.get_prices('WEGE3', date(day=1, month=7, year=2020))
print(test)
