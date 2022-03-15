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


# test()


def test2():
    import requests
    url2 = "https://api.hgbrasil.com/finance/stock_price?key=d53e6b41&symbol=vale3"
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=WEGE3.SA&interval=30min&apikey=LTW7TOI3RMVHE9OM&outputsize=compact '
    r = requests.get(url2)
    data = r.json()

    print(data)


# test2()


def test_scrap():
    import requests
    from bs4.element import Tag, ResultSet
    from bs4 import BeautifulSoup

    # https://statusinvest.com.br/home/mainsearchquery?q=localiza
    # https://statusinvest.com.br/img/company/cover/246.jpg
    # https://statusinvest.com.br/img/company/avatar/246.jpg

    url = 'https://statusinvest.com.br/acoes/rent3'
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')

    # print(html.prettify())

    _tag: Tag = html.find('button', attrs={'id': 'btn-resume-wallet'})
    print(_tag.get('data-parentid'))
    print(_tag.get('data-code'))
    print(_tag.get('data-name'))

    rs: ResultSet = html.select('.special > div:nth-child(1) > div:nth-child(1) > strong:nth-child(3)')

    _tag: Tag = rs.pop()
    print(_tag.text)

    rs: ResultSet = (
        html.select(
            'div.top-info-md-n:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)'))

    _tag: Tag = rs.pop()
    a = _tag.find('a')
    href = a.get('href')

    setor = a.find('strong', attrs={'class': 'value'})
    print(href, setor.text)

    rs: ResultSet = (
        html.select(
            'div.pl-md-2:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)'))

    _tag: Tag = rs.pop()
    a = _tag.find('a')
    href = a.get('href')

    subsetor = a.find('strong', attrs={'class': 'value'})
    print(href, subsetor.text)

    rs: ResultSet = (
        html.select(
            'div.pl-md-2:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)'))

    _tag: Tag = rs.pop()
    a = _tag.find('a')
    href = a.get('href')

    segmento = a.find('strong', attrs={'class': 'value'})
    print(href, segmento.text)

    resp = requests.get('https://statusinvest.com.br/home/mainsearchquery?q=localiza')
    data = resp.json()
    print(data)


# test_scrap()

def down_image():
    import requests

    img_data = requests.get('https://statusinvest.com.br/img/company/avatar/246.jpg').content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)


def locate_cotacao(codigo: str):
    import yfinance as yf
    import pandas as pd

    precos = pd.DataFrame()
    precos[0] = yf.download('VALE3.SA', start='2022-03-09', end='2022-03-10')
    return precos

down_image()