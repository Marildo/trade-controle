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
            # 'X-CAPTCHA': '03AFcWeA7AqOTWcb_v6-V-ckRN19XNJr3I_xrU5-UFkVWHE7ObEBHySjCCKY8TRSvJRmMx45XM6pNCF4t4IMPKeqGRKOphoLv29LWcxnUxODoHhUeSKzxG9gIZvN5fnKYq6OyFnRWHO7ak5wLnizqkEhu_FsdNxGUJHG7LWDJbx0OpPRI6D9ZYmWI5xZCcdgSxMY0BgY2OLU0BOa-hs5hRXZV9MmRRemzI8E5fNOPpw0n9vlb88-KiGHcj-UWfPu4lVKRPekEgO4zUgljNBLwQXC9ImzKd7rdwJWEIzAZMqeMPZXVtvxKZNSR8TYcOJgMfNTSkxx2h2HesM046uAtHCdLa6YSTuG8Uh_9ssY_vK5ClZUvqPWnAzPYF2ZGmL2heuuEQnNvmt6okfgaN3kCAUEpxKQzHLlbGYJQFTiAsnJRtX6SGC0sDsBwkQgU7TtzWFsxDh3XeTIVK-c3nXqKD4DvhDLe9MQOXLcsORZsm2helQEP-ZyAUzXJ6UBUpZkMHV7GKjCU74jKbKnibNcCJgI9b0LMJSZsl9vueWcyWJkTwfU9-4IV8jiZh_qldNj7gySS-goACnKvSqxWoTN8zZiJjERGwSiPdte21mwOQ68lBcveGXCK73UieSGBWA2anuETenvEC8DSFbf67ZaKT6UMU2T7io0x6JWnfaLSxucSEAsb1xCUBXfSoE52igRBehkYOca2S-jGPFUaPhlEIe9_w1HGEI9fXBqDj5Obeo1qeRXLkQ76UaCsjsov-TlSIt8IB_7E0lRcXyWzJ3oNtYGFu6eF0RkHRxZ14MB2JHpKs_vxXAd7K1EPAXnzy_27KfwOMqFcTKuZz6re9EsfK5Ul_YacGosbwrpfUatgS8bdiUtbhvIo-AYAbvUmElXFyN2T0rnbNED-3_lJWi-ASFw8A4coVpsweJ3yOn4uslZY8ZIimiB4MHdDKJeqPAJBdgRPP6TvbMRHwnGYIbOC3rjoqOBCMY6k5_lwXcWJ_ZzJeT6tip_xxbJwVgkp5TpMs0PokSC8u6f0gEHosy7_gAZUgZGqmU2p4qjqjlX8iGpdYWC-kIN6CmPH59eN4ESIKJax5-P8YD6nv7UA67Zr2fRJIQlFALAGTu2T50TKMaA229DIYeakwAi0YZubnKwQ5sknvwDrEDIplGhDFWPyGiAXQZ-X40a8v0YWwIDvfPrHlXGyu3B2iElKhA8y3Moc-dy0SdraqaFLOCArxfIKvTEIek7niNcy8e9ypz0IDzGWhNDSliB_gcpx3zORlADkgCQVmolnA9GVIRhUrhnMsV6OAa6sETEAz86K3TZ1BjTcCF0A2p1FfceQAocjSvI9PNSO2DTA8Bp0WTlQZ1Ong0Q6yarldO50OhVBV_zHeKoBQxirBa5XQK7TKuHTD30VV4_bUYMPdXSOmCCp6TNaCskJ9HZgAzQuFM6s80oadChwpARIMPkYT87C5AgIhlGfDg1e9N9aFwtto1i0hPeLAMO2q5hRlEyCe6ts3cKwKKuSZ9RpCC4GJNJuyRrbXuK1WMAgPUlD2FzOPv6wYZ39ufboxv3aKeuf5t9gx-8FRutLjQ0s9ztXLHGJCJseckOc6G7JNDU7R9iBotvhskzYpA0tV6mGxmPz5HEWF8DdBecIZhlAbsk74P_VsgHiBbgTAPk7jwtZ8JOkHcc2qMvEMlcS78GfG5E7OhTCTRYkUgml0SVmueSRy838',
            # 'X-CAPTCHA-SITEKEY': '6LeCsxUgAAAAAIEdUujNlJ145lIdWK-hE4HI1wl5'
        }
        payload = '&'.join([f'{k}={v}' for k, v in data.items()])
        logger.info(payload)

        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            # 'X-Sessionid': 'd547e759-8dd1-4a0d-96b8-8af75ba64c07',
            # 'X-Toro-Platform-Identifier': '1d4bc2e8ec8a9f8f3b94580bbfd97e16',
            'X-Toro-Platform-Origin': 'HubToro'
        }

        payload='username=07002842650&password=Lm%24318798&client_id=Hub&grant_type=password&X-TOKEN=92414&X-TOKEN_TYPE=TokenTime&X-TOKEN_CATEGORY=Monthly&X-CAPTCHA=03AFcWeA4646kSj2in3Qn8PjXB8TTIcvce7NA8olrFVXrz_7xGZPa_qAyii-PRxK1zhgVWtsR9HioiBBbKcmFf_oahSLb4ElgV_nznCx3IQiBh8v3Eov-UOGHCyXGAl5G7hlLJ3eMEnSy2uDW6OkFk_oKv4_FxJIoOxwGqNEVtQVinNINnv_G5ra6yBNZbpxuKYF8Jju0nA2sqWJQwl3AHDcAsZv-anOCik-qgcQxL0lW_w_BEUoTKllNSp04AsAEV8sezMOA_WFKt-ULgUpx1eEsI0HuxNjkEmdvmBbnQTTF-GZT2tAITlQhhnTfTZLPl-VMdsNudRBGMBxtQyHWls4ikkGVudfnDjgn8ySjOzHIX15WjoVTLmOYVbj-VrDpLxNTMqPZrF-dw3jlYNt-G_cwPe0oXwqypnrdptYXRNBU098OpM-5AUUbrZbewkQ3nLhACgHrEOgFv3IAl_qP0psPPo4Sdqm9o8zUDT4kdV-PKZGWkJvROzsPtUx1AXni5K2xY5hhxx0P58zuH89s-sh5dJBMWUTMdxtuWLIfyJIsRs1-q9BAqbKg3lD29a39wOI01BEnx6ikf3EQlNjYCyszZE0Js1Dpvieg_9NGTagaUqwa2eagl5qIZryfXxV4cY9UqsTI15IIVKU7KlcHmw51lXmu06nx4YA9L3wsTtVEDEcGzQhF5sGTIYECDD_07moshikmWzX9cBXtFajvZC2VckQH2wDF7k08YBkwUMEWoRWJ1AgUAOdXj46Z4IOj6V1bKwiH8a9oM1sGsJpWKybwZztCseXgicXNq1aHkOMdG72gR1COn1SWHVNheC86jmiesLAFv_07X4z6wGiBWhiUXCPU6MonO2nwjWg15YgakoB0q1-jNJpocBQKj5j_B92uAqqP56SFPbY5pK_iHe9DjK99khvztAB-zjYqJOcYG0pvN2msKnt_58Adxx6sgKw4m2_Z3OWpkV2wg3ZVtRCynbZepZqVp9yR5w2uJNz7EfbSRlVEzAlkham9sIgySVsqE0_v66WBS0EzTEqth0xXHNyMwvRv_TZY0sNSGfd6sL28QZ8XJGuEUnvI56IZrUDF74GqsSPeXb6NQiVE-ZnrxE-tHsFprZnREXTq2WQqSd0xnExqYi8-Fw_Mq1hZ-Pta0-bN88lBMuFgMAjqNTQVpii_ge7DvWBDj3n9ARSJNSEaThLFIRdcBH9UynzD9jSaZ3BKJHrtAHJsJjBDz9fOApkcUR6gPtmKnmvm9UyY7X-0tIIPAKMsbXHLLWmsGai02O6-hKn357fM12Zob7GTFT9MiVtCHob7AmExhgnq2lGRkmPZwvdY4a9Fmcl_R2hUbrVk5jdcND7-YlLZVX3Umi_8-pPjJZvsMYernsDMg38uwzmMMVf72Zh1CC4hYau-Dx4XAXtCEHp-dKwmj0iMyAYqS1emWZvF2ZGB0nto0Bb2pb9DCIR7mqb6tk6xTKCwn4td1Ldo3CNqz4eQfSRJoBt9WOzeyU-dz4NUQcyGRYY6lfQh1i1PUFs3MLrH9P5tJ9Dt5SO4M8eOHZBe_MUkDcDm0GOWAQeBZIW5aZi0KVZa3SlMHM40UJvCdjWiQ1oEgU6ti7M7LodWFvGqnqUB1OebDMyMk5aVVWV6y7fjTLkEs8Z9vTJvx3hLwhX1mo_FlnVa2NTmAdPsFxkZa5XRYZnikQBRxPKC2l2JrrzuVMaRz0zRa2tg&X-CAPTCHA-SITEKEY=6LeCsxUgAAAAAIEdUujNlJ145lIdWK-hE4HI1wl5'


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
