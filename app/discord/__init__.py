import requests


API_ENDPOINT = 'https://discord.com/api'


def call(url: str, method=None, data: dict = None, headers: dict = None) -> requests.Response:
    if url.startswith('/'):
        url = API_ENDPOINT + url
    method = method or ('POST' if data else 'GET')
    return requests.request(method, url, json=data, data=data, headers=headers)


from .auth import login, get_login_url
