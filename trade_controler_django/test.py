"""
Created on 10/03/2022
by MarildoCesar

https://web.dio.me/articles/consumindo-uma-api-de-cotacao-de-ativos-da-bolsa-de-valores?page=1&order=oldest
LTW7TOI3RMVHE9OM

https://hgbrasil.com/apis/cotacao-acao/b3-brasil-bolsa-balcao-b3sa3
"""


def test():
    import yfinance as yf

    x = yf.download('WEGE3.SA', start='2022-03-08', end='2022-03-10')

    keys = x.keys().values

    days = {}
    for index, row in x.iterrows():
        data = {}
        days[index] = data
        for i in keys:
            y = row[i]
            data[i] = y


    print(days)

#test()


def test2():
    import requests
    url2 ="https://api.hgbrasil.com/finance/stock_price?key=d53e6b41&symbol=vale3"
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=WEGE3.SA&interval=30min&apikey=LTW7TOI3RMVHE9OM&outputsize=compact '
    r = requests.get(url2)
    data = r.json()

    print(data)

test2()