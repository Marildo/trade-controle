# @author Marildo Cesar 05/10/2024
import requests

# Defina seu cabeçalho da API do RapidAPI

headers = {
    'x-rapidapi-key': "287fc8cd68mshf151f0aed3213f7p110806jsn2af596a68845",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

# Função para buscar dados fundamentalistas de uma ação

def buscar_dados_fundamentalistas(ticker):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"
    querystring = {"symbol": ticker}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        dados = response.json()

        # Extraindo dados fundamentais importantes
        pe_ratio = dados['defaultKeyStatistics'].get('trailingPE', {}).get('fmt', None)
        roe = dados['financialData'].get('returnOnEquity', {}).get('fmt', None)
        profit_margin = dados['financialData'].get('profitMargins', {}).get('fmt', None)

        # Imprimindo os resultados
        print(f"Dados Fundamentalistas de {ticker}:")
        print(f"  - P/L (P/E Ratio): {pe_ratio}")
        print(f"  - ROE (Retorno sobre Patrimônio): {roe}")
        print(f"  - Margem de Lucro: {profit_margin}")
        print("\n")
    else:
        print(response.text)
        print(f"Erro ao consultar os dados da ação {ticker}")


# Consultar dados de CYRE3 e VALE3
buscar_dados_fundamentalistas("CYRE3.SA")
buscar_dados_fundamentalistas("VALE3.SA")
