import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    api_short_link = 'https://api.vk.ru/method/utils.getShortLink'

    payload = {
        'access_token': token, 
        'url': url, 
        'private': 0, 
        'v': '5.199'
        }
    response = requests.get(api_short_link, params=payload)
    response.raise_for_status()
    link = response.json()
    if 'response' in link:
        return link['response']['short_url']


def count_clicks(token: str, link: str) -> int:
    api_count_clicks = 'https://api.vk.ru/method/utils.getLinkStats'

    payload = {
        'access_token': token,
        'key': link,
        'source': 'vk_cc',
        'interval': 'forever',
        'intervals_count': 1,
        'extended': 0,
        'v': '5.199',
    }
    response = requests.get(api_count_clicks, params=payload)
    response.raise_for_status()
    response_json_obj = response.json()
    number_of_view = response_json_obj["response"]["stats"][0]["views"]
    return number_of_view


def is_shorten_link(token: str, url: str) -> bool:
    parameters = {
        'key': url,
        'interval': 'forever',
        'access_token': token,
        'v': '5.199'
    }
    response = requests.get(
        'https://api.vk.com/method/utils.getLinkStats', params=parameters)
    response.raise_for_status()
    return 'error' not in response.json()


def main():
    user_input = input('Введите ссылку: ')
    link = urlparse(user_input).path[1:]

    load_dotenv('Token.env')
    token = os.environ['VK_API_TOKEN']

    try:
        if is_shorten_link(token, link):
            number_of_view = count_clicks(token, link)
            print('Количество переходов по ссылке: ', number_of_view)
        else:
            short_link = shorten_link(token, user_input)
            print(short_link)
    except requests.exceptions.RequestException as error:
        print("Can't get data from server:\n{0}".format(error))


if __name__ == '__main__':
    main()
