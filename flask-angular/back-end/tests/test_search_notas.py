# @author Marildo Cesar 22/03/2024

import requests

url = "http://127.0.0.1:7300/notas/arquivos/search"

payload = {}
headers = {}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.status_code)