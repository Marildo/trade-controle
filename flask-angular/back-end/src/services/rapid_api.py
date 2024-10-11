# @author Marildo Cesar 05/10/2024
import requests


class RapidAPI:
    def __init__(self):
        self.headers = {
            'x-rapidapi-key': "287fc8cd68mshf151f0aed3213f7p110806jsn2af596a68845",
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    def buscar_dados_fundamentalistas(self, ticker: str):
        url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"
        querystring = {"symbol": ticker + '.SA'}

        response = requests.get(url, headers=self.headers, params=querystring)
        print(f'Rapid API info {ticker}', 'status code', response.status_code)
        if response.status_code == 200:
            response.raise_for_status()
            dados = response.json()

            # Extraindo dados fundamentais importantes
            pe_ratio = dados['defaultKeyStatistics'].get('trailingPE', {}).get('fmt', None)
            roe = dados['financialData'].get('returnOnEquity', {}).get('fmt', None)
            profit_margin = dados['financialData'].get('profitMargins', {}).get('fmt', None)

            def adj_value(value):
                if not value:
                    return None
                return value.replace('%', '').replace(',', '')

            return {
                'ticker': ticker,
                'preco_lucro': adj_value(pe_ratio),
                'roe': adj_value(roe),
                'margem_liquida': adj_value(profit_margin)
            }

        return None
