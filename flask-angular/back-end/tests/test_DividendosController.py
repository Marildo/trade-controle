# @author Marildo Cesar 19/09/2023


import requests

res = requests.put('http://127.0.0.1:7500/dividendos/process')
print(res.json())
