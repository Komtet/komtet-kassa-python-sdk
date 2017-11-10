# coding: utf-8
import decimal
import functools
import hashlib
import hmac
import json
from collections import namedtuple

import requests

DEFAULT_HOST = 'https://kassa.komtet.ru'

Task = namedtuple('Task', 'id external_id print_queue_id state')
TaskInfo = namedtuple('TaskInfo', 'id external_id state fiscal_data error_description')


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(JSONEncoder, self).default(obj)


json_encode = functools.partial(json.dumps, cls=JSONEncoder)


class Client(object):
    """
    :param str shop_id: Идентификатор магазина
    :param str secret_key: Секретный ключ
    """

    def __init__(self, shop_id, secret_key):
        self.__host = DEFAULT_HOST
        self.__shop_id = shop_id
        self.__secret_key = secret_key.encode('utf-8')
        self.__default_queue = None

    def set_host(self, host):
        """
        :param str host: Хост в формате ``scheme://hostname.com``
        """
        self.__host = host
        return self

    def set_default_queue(self, qid):
        """
        Устанавливает идентификатор очереди, используемый по умолчанию.

        Этот идентификатор будет использоваться при вызове
        ``is_queue_active`` и ``create_task`` в случае,
        если идентификатор очереди не был указан.

        :param int qid: Идентификатор очереди
        """
        self.__default_queue = qid
        return self

    def is_queue_active(self, qid=None):
        """
        Является ли очередь активной

        :param int qid: Идентификатор очереди
        """
        qid = self.__handle_queue_id(qid)
        rep = self.__get('/api/shop/v1/queues/%s' % qid)
        rep.raise_for_status()
        return rep.json().get('state') == 'active'

    def create_task(self, check, qid=None):
        """
        Постановка задачи в очередь на фискализацию

        :param Check check: Экземпляр чека
        :param int qid: Идентификатор очереди
        """
        qid = self.__handle_queue_id(qid)
        rep = self.__post('/api/shop/v1/queues/%s/task' % qid, dict(check))
        rep.raise_for_status()
        result = rep.json()
        return Task(**result)

    def get_task_info(self, task_id):
        """
        Возвращает информацию о поставленной на фискализацию задаче

        :param str|int task_id: ID задачи
        """
        rep = self.__get('/api/shop/v1/tasks/%s' % task_id)
        rep.raise_for_status()
        result = rep.json()
        return TaskInfo(**result)

    def __handle_queue_id(self, qid):
        if qid is None:
            if self.__default_queue is None:
                raise ValueError('Queue ID is not specified')
            qid = self.__default_queue
        return qid

    def __get_url(self, path):
        return '{}/{}'.format(self.__host, path.strip('/'))

    def __get_signature(self, *args):
        return hmac.new(self.__secret_key, ''.join(args).encode('utf-8'), hashlib.md5).hexdigest()

    def __get(self, path):
        url = self.__get_url(path)
        headers = {
            'Authorization': self.__shop_id,
            'Accept': 'application/json',
            'X-HMAC-Signature': self.__get_signature('GET', url)
        }
        return requests.get(url=url, headers=headers, allow_redirects=True)

    def __post(self, path, data):
        url = self.__get_url(path)
        data = json_encode(data)
        headers = {
            'Authorization': self.__shop_id,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-HMAC-Signature': self.__get_signature('POST', url, data)
        }
        return requests.post(url=url, headers=headers, data=data)
