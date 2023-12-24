"""
 @author Marildo Cesar 24/06/2023
"""

from datetime import date
from io import BytesIO
from typing import Dict, List

import requests
from dateutil import parser
from werkzeug.datastructures import FileStorage

from src.settings import config, logger


class ToroService:

    def __init__(self, single_date: bool = False):
        self.__token = None
        self.single_date = single_date

    def process_corretagem(self, start_date: date) -> List[FileStorage]:
        list_dates = self.__list_date(start_date)
        result = []
        for nota in list_dates:
            result.append(self.__process_date(nota))

        return result

    def __authenticate(self):
        self.__token = config.toro_token
        if self.__token is not None:
            return

        url = "https://webapieqr.toroinvestimentos.com.br/auth/authentication/login"
        data = {
            'username': config.load_value('TR_USER_NAME'),
            'password': config.load_value('TR_PASSWORD'),
            'X-TOKEN': config.load_value('TR_X-TOKEN'),
            'client_id': 'Hub',
            'grant_type': 'password',
            'X-UserIP': '172.16.7.143',
            'X-TOKEN_TYPE': 'TokenTime',
            'X-TOKEN_CATEGORY': 'Monthly'
        }
        payload = '&'.join([f'{k}={v}' for k, v in data.items()])
        logger.info(payload)
        headers = {'Content-Type': 'text/plain'}
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        self.__token = data['access_token']
        config.set_token(self.__token, data['expires_in'])

    def __process_date(self, nota: Dict) -> FileStorage:
        base_url = 'https://webapieqr.toroinvestimentos.com.br/finance/brokeragenote/'
        market = nota['market'].lower()
        url = f"{base_url}{market}?referenceDate={nota['referenceDate']}"
        headers = {'Authorization': f'Bearer {self.__token}'}
        response = requests.request("GET", url, headers=headers, data={})
        response.raise_for_status()
        file_buffer = BytesIO(response.content)
        file_storage = FileStorage(file_buffer)
        file_storage.filename = f"{nota['referenceDate']}_{market}.pdf"
        return file_storage

    def __list_date(self, start_date) -> List:
        self.__authenticate()
        url = "https://webapieqr.toroinvestimentos.com.br/finance/note/listdate"
        headers = {'Authorization': f'Bearer {self.__token}'}
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()
        data = response.json()['value']
        for item in data:
            item['referenceDate'] = parser.parse(item['referenceDate']).date()

        dates = []
        for i in data:
            if i['referenceDate'] > start_date:
                dates.append(i)
                if self.single_date:
                    break

        dates = sorted(dates, key=lambda x: x['referenceDate'])
        return dates
