# @author Marildo Cesar 05/10/2024

import requests


# Função para consultar dados fundamentalistas de uma ação usando a API do Brapi
def consultar_dados_fundamentalistas(ticker):
    url = f'https://brapi.dev/api/quote/{ticker}'

    params = {
        'fundamental': 'true',
        'token': '2NAtghodcw37teHMnGKtf8',
    }

    response = requests.get(url, params)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        dados = response.json()

        print(dados)

        # Extrair os dados relevantes da resposta
        acao = dados['results'][0]
        nome = acao['symbol']
        preco_atual = acao['regularMarketPrice']

        pl = acao['priceEarnings']
        # roe = acao['financialData']['returnOnEquity']
        # margem_liquida = acao['fundamentals']['netMargin']

        # Exibir os dados
        print(f"Dados fundamentalistas da ação {nome}:")
        print(f"Preço Atual: R${preco_atual}")
        print(f"P/L (Preço/Lucro): {pl}")
        print(f"ROE (Retorno sobre Patrimônio): {roe}%")
        print(f"Margem Líquida: {margem_liquida}%\n")
    else:
        print(response.text)
        print(f"Erro ao consultar dados para {ticker}")


# Consultar dados para CYRE3 e VALE3
consultar_dados_fundamentalistas('CYRE3')
consultar_dados_fundamentalistas('VALE3')
