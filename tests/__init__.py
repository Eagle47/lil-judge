import requests

BASE_URL = 'http://localhost:5000'


def post(url, payload, token=None):
    headers = {'X-Auth-Token': token} if token is not None else None
    return requests.post(BASE_URL + url, json=payload, headers=headers).json()


def get(url, token = None):
    headers = {'X-Auth-Token': token} if token is not None else None
    return requests.get(BASE_URL + url, headers=headers)