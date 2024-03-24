"""
 @author Marildo Cesar 24/06/2023
"""

from datetime import date
from io import BytesIO
from typing import Dict, List

import requests
from dateutil import parser
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest
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
            'client_id': 'Hub',
            'grant_type': 'password',
            'X-TOKEN': config.load_value('TR_X_TOKEN'),
            'X-TOKEN_TYPE': 'TokenTime',
            'X-TOKEN_CATEGORY': 'Monthly',
            'X-CAPTCHA': '03AFcWeA7AqOTWcb_v6-V-ckRN19XNJr3I_xrU5-UFkVWHE7ObEBHySjCCKY8TRSvJRmMx45XM6pNCF4t4IMPKeqGRKOphoLv29LWcxnUxODoHhUeSKzxG9gIZvN5fnKYq6OyFnRWHO7ak5wLnizqkEhu_FsdNxGUJHG7LWDJbx0OpPRI6D9ZYmWI5xZCcdgSxMY0BgY2OLU0BOa-hs5hRXZV9MmRRemzI8E5fNOPpw0n9vlb88-KiGHcj-UWfPu4lVKRPekEgO4zUgljNBLwQXC9ImzKd7rdwJWEIzAZMqeMPZXVtvxKZNSR8TYcOJgMfNTSkxx2h2HesM046uAtHCdLa6YSTuG8Uh_9ssY_vK5ClZUvqPWnAzPYF2ZGmL2heuuEQnNvmt6okfgaN3kCAUEpxKQzHLlbGYJQFTiAsnJRtX6SGC0sDsBwkQgU7TtzWFsxDh3XeTIVK-c3nXqKD4DvhDLe9MQOXLcsORZsm2helQEP-ZyAUzXJ6UBUpZkMHV7GKjCU74jKbKnibNcCJgI9b0LMJSZsl9vueWcyWJkTwfU9-4IV8jiZh_qldNj7gySS-goACnKvSqxWoTN8zZiJjERGwSiPdte21mwOQ68lBcveGXCK73UieSGBWA2anuETenvEC8DSFbf67ZaKT6UMU2T7io0x6JWnfaLSxucSEAsb1xCUBXfSoE52igRBehkYOca2S-jGPFUaPhlEIe9_w1HGEI9fXBqDj5Obeo1qeRXLkQ76UaCsjsov-TlSIt8IB_7E0lRcXyWzJ3oNtYGFu6eF0RkHRxZ14MB2JHpKs_vxXAd7K1EPAXnzy_27KfwOMqFcTKuZz6re9EsfK5Ul_YacGosbwrpfUatgS8bdiUtbhvIo-AYAbvUmElXFyN2T0rnbNED-3_lJWi-ASFw8A4coVpsweJ3yOn4uslZY8ZIimiB4MHdDKJeqPAJBdgRPP6TvbMRHwnGYIbOC3rjoqOBCMY6k5_lwXcWJ_ZzJeT6tip_xxbJwVgkp5TpMs0PokSC8u6f0gEHosy7_gAZUgZGqmU2p4qjqjlX8iGpdYWC-kIN6CmPH59eN4ESIKJax5-P8YD6nv7UA67Zr2fRJIQlFALAGTu2T50TKMaA229DIYeakwAi0YZubnKwQ5sknvwDrEDIplGhDFWPyGiAXQZ-X40a8v0YWwIDvfPrHlXGyu3B2iElKhA8y3Moc-dy0SdraqaFLOCArxfIKvTEIek7niNcy8e9ypz0IDzGWhNDSliB_gcpx3zORlADkgCQVmolnA9GVIRhUrhnMsV6OAa6sETEAz86K3TZ1BjTcCF0A2p1FfceQAocjSvI9PNSO2DTA8Bp0WTlQZ1Ong0Q6yarldO50OhVBV_zHeKoBQxirBa5XQK7TKuHTD30VV4_bUYMPdXSOmCCp6TNaCskJ9HZgAzQuFM6s80oadChwpARIMPkYT87C5AgIhlGfDg1e9N9aFwtto1i0hPeLAMO2q5hRlEyCe6ts3cKwKKuSZ9RpCC4GJNJuyRrbXuK1WMAgPUlD2FzOPv6wYZ39ufboxv3aKeuf5t9gx-8FRutLjQ0s9ztXLHGJCJseckOc6G7JNDU7R9iBotvhskzYpA0tV6mGxmPz5HEWF8DdBecIZhlAbsk74P_VsgHiBbgTAPk7jwtZ8JOkHcc2qMvEMlcS78GfG5E7OhTCTRYkUgml0SVmueSRy838',
            'X-CAPTCHA-SITEKEY': '6LeCsxUgAAAAAIEdUujNlJ145lIdWK-hE4HI1wl5'
        }
        payload = '&'.join([f'{k}={v}' for k, v in data.items()])
        logger.info(payload)

        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            # 'X-Sessionid': 'd547e759-8dd1-4a0d-96b8-8af75ba64c07',
            # 'X-Toro-Platform-Identifier': '1d4bc2e8ec8a9f8f3b94580bbfd97e16',
            'X-Toro-Platform-Origin': 'HubToro'
        }

        payload='username=07002842650&password=Lm%24318798&client_id=Hub&grant_type=password&X-TOKEN=45224&X-TOKEN_TYPE=TokenTime&X-TOKEN_CATEGORY=Monthly&X-CAPTCHA=03AFcWeA4Kpuzn_mwrs8mMTFu8IouIAFjWvYqUwFXMj_IZPZFlAyJ1a5h2NmYOpHLP3DcQ_axJ_IDIyIbWCLyHUAe2LnsFe1-4L9OW_COJRwVYYnkJtn5QGvwnrFLR3zRJUuhdjWMQPX2dbTW_S9mMfViKIwtSYI0RDKnVLkptQmVsQ0iSgcApqRsZT7xThkzG5dhV1r4wXqDN7wU6r5tctZiW1njXXXyWrGaZnuzhBQwkj7nnDUHznAnJsDv1ruCSnLSoThclHQ2KmZoiEp_d0_49nzedy6v0Mjgta-Ntc2H5fytUT45vQioRY8omZ-64sUevT8ev_Trc6m-iHoWX5bt9E4jJNkk5B4_MQNwLdZ321nvEO6sKlpcFb9Xxby8BqTzmE3XFB-EVw-FvkubC-DuNyL9vh4SRZJggBL-wp2vZe6ETGVm0kQN-JoDSvdjgyAZ8wfvgYncleScCYWFaf993BS4HEoo0sESpJ4_FhX0aXZOGEopcE04KlVtkYQGhUkxNM5gI2-cb9JPLG9LYACtxM3Hz85XNFKGXR4xb0GcrI5Bxvk8AautlTzVLK0LBUOxdp03BI6-9rmxTu1UPYP7XWdqzsFRee-AE6tRIo2f4ISKC4jeuVES70cqo9w-ab5HR9FqOQq8ThsltsVHff9u451ByfsoQDLOvmXgzLGtinw5L8GcGIVpofbx9ukIE08Fnsh9MJKZKlfyJeQS3DB8anm0ldj153hai7xPiNXAXVhCmyXFY9LIwYHncDWYLOw63pB_9XJ9uESTEpXfZqXZG2WPVsKgaQpkhgBTnbGYuX5lGIIV0lh7sLCr_hSNfZRFJzp6KXMvICY0bVp5L3rDfsAvyysvEKRhSU0SqQdOwTLfXhXw7hl3ICaZks_ulAtac06159hVPBP2uwQU0dqa3JIl-4tcjxp87C9KWiU-fwrgsHOAaq4qM9DzZ-fEfnQVSfFNpwMm_7YNagnNoeC5I9lu69JqjEYCynZrdV6-bggclTUTiB5cGCNiCZd5ScV_fvXOp7f_GO8SyFW0DnZ0FOYKEqOmqj-zMgA5ZdZ_bbc31eqYK_lPwCtRE2onm5UJEj1OLtxiLUGiBLIHInVNrKLlAwxgfBF1Szgi1RNtNqkQgut542uUbdpx-9idgzkfiboWHuqYC0pc3bdsOs1obUx9zO8qi6szMkHNILZKjPQHdlBZ8e47fib0-TST4SXt4oMKzyT_I0rwvht5IsKzssIJ_DAnEv9Dw5ns-2hKeGAYr5BDG5BAGoruaFHnss_DxJoRM4gPVy-pOwD-ZfftxYaKukfkxVjE8Syr5BAXafL9bk5tmN4P3lJXlKcbOsu50XCofCrutperhtejeSVeaByRVi1W73lV1m_KlxJL1hP0n4h8sWm_ysyu2TFT6HNWojw-GSeqP4Ut7ZJAx0C3psIQp6nmbmQfGy4dyuWFdwfktp7UkT6kB7lAbUFTCJRtqQcKCtnfNiQKz3jikDApkyNkk3GHWHYOc-Afj9WdZjh080nely009hNA9wYarO2aWoDNZipR-rsXtqhsRMr7W5O0isEAEpsVdJVaaJX2v7dDvyZo6EucN9xld-yiaVT2otHi33JgEzMmS9LUM52Vg_mLXIE3TxTHTZUJ1ky7-MBj1JJwhLS8_1R7M23G6KsHtQ_GWSOqbaIuGc_C_IcZkt-h-IMBzc3PtMLFD8KpUyFvIjYyVU3s&X-CAPTCHA-SITEKEY=6LeCsxUgAAAAAIEdUujNlJ145lIdWK-hE4HI1wl5'


        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise BadRequest('Falha ao realizar login na Toro')
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
            if start_date < i['referenceDate'] < date.today():
                dates.append(i)
                if self.single_date:
                    break

        dates = sorted(dates, key=lambda x: x['referenceDate'])
        return dates
