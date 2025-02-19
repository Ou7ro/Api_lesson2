import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


class ApiExceptionError(Exception):
    def __init__(self, message: str, error_msg):
        message = f'Api error: {error_msg}'
        super().__init__(message)


def shorten_link(token: str, url: str):
    api_short_link = 'https://api.vk.ru/method/utils.getShortLink'

    payload = {
        'access_token': token,
        'url': url,
        'private': 0,
        'v': '5.199',
        }
    response = requests.get(api_short_link, params=payload, timeout=10)
    response.raise_for_status()
    response_answer = response.json()
    response_answer = response.json()
    if 'error' in response_answer:
        raise ApiExceptionError('Api error: ', response_answer['error']['error_msg'])
    return response_answer


def count_clicks(token: str, url: str):
    api_count_clicks = 'https://api.vk.ru/method/utils.getLinkStats'

    payload = {
        'access_token': token,
        'key': url,
        'source': 'vk_cc',
        'interval': 'forever',
        'intervals_count': 1,
        'extended': 0,
        'v': '5.199',
    }
    response = requests.get(api_count_clicks, params=payload, timeout=10)
    response.raise_for_status()
    short_link = response.json()
    if 'error' in short_link:
        raise ApiExceptionError('Api error: ', short_link['error']['error_msg'])
    return short_link


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
    parsed_url = urlparse(user_input).path[1:]

    load_dotenv('Token.env')
    token = os.environ['VK_API_TOKEN']

    try:
        if is_shorten_link(token, parsed_url):
            number_of_view = count_clicks(token, parsed_url)
            print('Количество переходов по ссылке: ', number_of_view["response"]["stats"][0]["views"])
        else:
            short_link = shorten_link(token, user_input)
            print(short_link['response']['short_url'])
    except ApiExceptionError as error:
        print(error)


if __name__ == '__main__':
    main()
