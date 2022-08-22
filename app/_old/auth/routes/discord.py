import urllib
from flask import redirect, request, url_for
from flask_login import login_user
import requests

from app import db, logger
from app.exceptions import APIError
from app.keys_manager import KeysManager
from app.models import DiscordAccount, User
from .. import bp

API_ENDPOINT = 'https://discord.com/api'
AUTHORIZE_ROUTE = 'oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&prompt=consent&scope={scope}'
SCOPES = [
    'identify',
    # 'email',
]

def get_auth_params(full=False, urlencode=None):
    if urlencode is None:
        urlencode = not full
    keys = KeysManager.get('discord')
    if keys is None or 'client_id' not in keys:
        raise APIError('Discord API credentials not found')
    url = url_for('.discord_callback', _external=True)
    if url.startswith('http://127.0.0.1'):
        logger.debug('Rewriting URL to localhost')
        url = 'http://localhost' + url[len('http://127.0.0.1'):]
    if urlencode:
        urllib.parse.quote(url, safe='')
    result = {
        'scope': '%20'.join(SCOPES),
        'redirect_uri': url,
        'client_id': keys.get('client_id'),
    }
    if full:
        result.update({'client_secret': keys.get('client_secret')})
    return result

def auth_from_code(code):
    data = get_auth_params(full=True)
    data.update({
        'grant_type': 'authorization_code',
        'code': code,
    })
    response = requests.post(f'{API_ENDPOINT}/oauth2/token', data=data)
    if not response.ok:
        logger.warning('Could not authorize user to Discord')
    return response.json()

@bp.route('/login/discord')
def discord_login():
    url = f'{API_ENDPOINT}/{AUTHORIZE_ROUTE.format(**get_auth_params())}'
    return redirect(url)

@bp.route('/login/discord/callback')
def discord_callback():
    next = redirect(url_for('main.home'))
    result = auth_from_code(request.args.get('code'))
    access_token = result.get('access_token')
    response = requests.get(f'{API_ENDPOINT}/oauth2/@me', headers={'Authorization': f'Bearer {access_token}'})
    if not response.ok:
        logger.warning('Could not authorize to Discord')
        return next
    user_response = response.json()['user']
    logger.info('User fetched from Discord API', user_response)
    id = int(user_response['id'])
    discord_account = DiscordAccount.query.get(id)
    if not discord_account:
        discord_account = DiscordAccount(id=id, access_token=access_token)
        user = User()
        user.set_avatar_from_discord(data=user_response)
        discord_account.user_id = user.id
        discord_account.user = user
        db.session.add(discord_account, user)
        next = redirect(url_for('main.welcome'))
    discord_account.access_token = access_token
    discord_account.refresh_token = result.get('refresh_token')
    if not discord_account.user._name:
        discord_account.user._name = user_response['username']
    db.session.commit()
    login_user(discord_account.user, remember=True)
    return next
