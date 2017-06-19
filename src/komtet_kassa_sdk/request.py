# -*- coding: utf-8 -*-
import hashlib
import hmac

from json import dumps

import six
import requests

from .utils import JSONEncoder


API_SERVER = 'http://kassa.komtet.ru'
API_PATH_PREFIX = '/api/shop/v1'

SHOP_KEY = None
SHOP_SECRET = None


def _prepare_param(val):
    if val is None:
        return ''
    elif isinstance(val, dict):
        return dumps(val, cls=JSONEncoder)

    return six.text_type(val)


def request(method, path, **kwargs):
    shop_key = kwargs.pop('shop_key', SHOP_KEY) or SHOP_KEY
    shop_secret = kwargs.pop('shop_secret', SHOP_SECRET) or SHOP_SECRET

    url = API_SERVER + API_PATH_PREFIX + path
    msg = method + url + _prepare_param(kwargs.get('params')) + _prepare_param(kwargs.get('data'))

    headers = {
        'Authorization': shop_key,
        'X-HMAC-Signature': hmac.new(shop_secret.encode('utf-8'), msg.encode('utf-8'), digestmod=hashlib.md5).hexdigest()
    }

    with requests.sessions.Session() as session:
        return session.request(method=method, url=url, headers=headers, **kwargs)


def get(path, params=None, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    return request('GET', path, params=params, **kwargs)


def post(path, data=None, json=None, **kwargs):
    data = dumps(json, cls=JSONEncoder)
    return request('POST', path, data=data, **kwargs)
