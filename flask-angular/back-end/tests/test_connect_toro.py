import requests

def login():
    url = "https://webapieqr.toroinvestimentos.com.br/auth/authentication/login"
    payload = "username=07002842650&password=Tr%40318798&client_id=Hub&grant_type=password&X-UserIP=172.16.7.143&X-TOKEN=19260&X-TOKEN_TYPE=TokenTime&X-TOKEN_CATEGORY=Monthly"
    headers = {
        'Content-Type': 'text/plain',
        'Cookie': 'AWSALB=JzXmYfHuesfGzLC6AhYSoB3+TU3kwVHOtnkCErA0CrRnH3lpW4JToVKriglyIEZkwXj+HjN7HfqFZHiSHoS19CTo6QwFI/NQQABAOr0a970TudJr7IHQRgnr8KeV; AWSALBCORS=JzXmYfHuesfGzLC6AhYSoB3+TU3kwVHOtnkCErA0CrRnH3lpW4JToVKriglyIEZkwXj+HjN7HfqFZHiSHoS19CTo6QwFI/NQQABAOr0a970TudJr7IHQRgnr8KeV'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response['access_token']


def download():
    future = "https://webapieqr.toroinvestimentos.com.br/finance/brokeragenote/future?referenceDate=2023%2F05%2F17"
    payload = {}
    headers = {
        'Authorization': 'Bearer '+login(),
       # 'Cookie': 'AWSALB=+K2HfI5jOfyt3yZ5M1N5tlhseRiUJxSEBMcATyqGOpKdMMnFtgdYcs7FoyratQ1eJprFeHoI6cDuQsbmvuQBls65fsPgAGBzNl5PLEPlg4bDRa8biPDn+BRuRiNz; AWSALBCORS=+K2HfI5jOfyt3yZ5M1N5tlhseRiUJxSEBMcATyqGOpKdMMnFtgdYcs7FoyratQ1eJprFeHoI6cDuQsbmvuQBls65fsPgAGBzNl5PLEPlg4bDRa8biPDn+BRuRiNz'
    }
    response = requests.request("GET", future, headers=headers, data=payload)
    with open('future.pdf', 'wb') as f:
        f.write(response.content)

download()