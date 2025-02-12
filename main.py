import requests


payload = {'access_token': 'ffdaef98ffdaef98ffdaef98a3fcf39bc2fffdaffdaef989871b4a5cedab68182bb53a8', 'v': '5.199'}
url = 'https://api.vk.ru/method/utils.getServerTime'
response = requests.get(url, params=payload)
response.raise_for_status()
print(response.text)
