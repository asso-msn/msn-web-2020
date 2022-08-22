import requests

from app import db

class DiscordAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    access_token = db.Column(db.String)
    refresh_token = db.Column(db.String)
    user = db.relationship('User')

    def call(self, url: str, method=None, data : dict = None, headers : dict = None) -> requests.Request:
        if url.startswith('/'):
            url = 'https://discord.com/api' + url
        headers = headers or {}
        headers['Authorization'] = f'Bearer {self.access_token}'
        method = method or ('POST' if data else 'GET')
        return requests.request(method, url, json=data, headers=headers)
