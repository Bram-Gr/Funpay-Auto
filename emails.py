import requests

url = "https://api.firstmail.ltd/v1/market/buy/mail?type=3"

headers = {
    "accept": "application/json",
    "X-API-KEY": "c5816a11-b9eb-4325-91d4-94f3179a4ea3"
}

response = requests.get(url, headers=headers)

print(response.text)