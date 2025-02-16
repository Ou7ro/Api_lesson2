import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    api_short_link = 'https://api.vk.ru/method/utils.getShortLink'
    
    response = requests.get(url)
    response.raise_for_status()

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

def count_clicks(token, link):
    api_count_clicks = 'https://api.vk.ru/method/utils.getLinkStats'
    response = requests.get(api_count_clicks)
    response.raise_for_status()

    payload = {
        'access_token': token,
        'v': '5.199',
        'key': link,
        'source': 'vk_cc',
        'access_key': '',
        'interval': 'forever',
        'intervals_count': 1,
        'extended': 0,
    }
    response = requests.get(api_count_clicks, params=payload)
    response.raise_for_status()
    response_data = response.json()
    clicks_data = response_data['response']['stats'][0]['views']
    return clicks_data

def is_shorten_link(token, url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = f'http://{url}'
        parsed_url = urlparse(url)
    parameters = {
        'url': url,
        'access_token': token,
        'v': '5.199',
    }
    response = requests.get(
        'https://api.vk.ru/method/utils.checkLink', params=parameters)
    response.raise_for_status()
    shortened_url_netlocs = ['vk.cc']
    parsed_url_netloc = parsed_url.netloc
    parsed_url_path = parsed_url.path[1:]
    is_short = parsed_url_netloc in shortened_url_netlocs
    if is_short and not parsed_url_path:
        raise Exception('Неверный формат ссылки')
    return is_short    

def main():
    user_input = input('Введите ссылку: ')

    load_dotenv('Token.env')
    token = os.environ['VK_API_TOKEN']

    try:
        if not is_shorten_link(token, user_input):
            short_link = shorten_link(token, user_input)
            print(short_link)
        else:
            link_key = urlparse(user_input).path[1:]
            print(f'Количество переходов по ссылке: {
                count_clicks(token, link_key)
                }')
    except requests.exceptions.HTTPError as error:
        print("Can't get data from server:\n{0}".format(error))

if __name__ == '__main__':
    main()