import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


class ApiExceptionError(Exception):
    def __init__(self, message: str, extra_info: dir):
        super().__init__(message)
        self.extra_info = extra_info


def exception_for_unvalidUrl(response):
    if 'error' in response:
        raise ApiExceptionError('Ошибка Api: ', response['error']['error_msg'])


def shorten_link(token, url):
    api_short_link = 'https://api.vk.ru/method/utils.getShortLink'

    payload = {
        'access_token': token,
        'url': url,
        'private': 0,
        'v': '5.199',
        }
    try:
        response = requests.get(api_short_link, params=payload, timeout=10)
        response.raise_for_status()
        response_answer = response.json()
        exception_for_unvalidUrl(response_answer)
    except ApiExceptionError as apierror:
        exit(f'{apierror}{response_answer['error']['error_msg']}')
    response_answer = response.json()
    if 'response' in response_answer:
        return response_answer['response']['short_url']


def count_clicks(token: str, url: str) -> int:
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
    try:
        response = requests.get(api_count_clicks, params=payload, timeout=10)
        response.raise_for_status()
        response_answer = response.json()
        exception_for_unvalidUrl(response_answer)
    except ApiExceptionError as apierror:
        exit(f'{apierror}, {response_answer['error']['error_msg']}')
    number_of_view = response_answer["response"]["stats"][0]["views"]
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
    parsed_url = urlparse(user_input).path[1:]

    load_dotenv('Token.env')
    token = os.environ['VK_API_TOKEN']

    try:
        if is_shorten_link(token, parsed_url):
            number_of_view = count_clicks(token, parsed_url)
            print('Количество переходов по ссылке: ', number_of_view)
        else:
            short_link = shorten_link(token, user_input)
            print(short_link)
    except requests.exceptions.HTTPError as error:
        print(f"Произошла ошибка: {error}")


if __name__ == '__main__':
    main()
