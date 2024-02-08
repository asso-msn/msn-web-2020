import requests

API_ENDPOINT = "https://discord.com/api/v10"


TYPES = {
    "form": "application/x-www-form-urlencoded",
}


def call(
    url: str,
    method: str = None,
    data: dict = None,
    headers: dict = None,
    token: str = None,
    bot: str = None,
    type: str = None,
) -> requests.Response:
    if url.startswith("/"):
        url = API_ENDPOINT + url
    method = method or ("POST" if data else "GET")
    if token or bot or type:
        headers = headers or {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if bot:
        headers["Authorization"] = f"Bot {bot}"
    if type:
        type = TYPES.get(type) or type
        headers["Content-Type"] = type
    return requests.request(method, url, json=data, data=data, headers=headers)


from .auth import get_login_url, login
