# coding: utf-8
import decimal
import functools
import hashlib
import hmac
import json

import requests


DEFAULT_HOST = 'https://kassa.komtet.ru'


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(JSONEncoder, self).default(obj)


json_encode = functools.partial(json.dumps, cls=JSONEncoder)


class Response(object):

    def __init__(self, **data):
        self.__data = data

    def __getattr__(self, name):
        return self.__data[name]

    def _asdict(self):
        return self.__data

    def __iter__(self):
        for item in self.__data.items():
            yield item


Task = TaskInfo = OrderInfo = EmployeeInfo = Response


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
        rep = self.__get('/api/shop/v2/queues/%s' % qid)
        rep.raise_for_status()
        return rep.json().get('state') == 'active'

    def create_task(self, check, qid=None):
        """
        Постановка задачи в очередь на фискализацию

        :param Check check: Экземпляр чека
        :param int qid: Идентификатор очереди
        """
        qid = self.__handle_queue_id(qid)
        rep = self.__post('/api/shop/v2/queues/%s/task' % qid, dict(check))
        rep.raise_for_status()
        result = rep.json()
        return Task(**result)

    def create_tasks(self, checks, qid=None):
        """
        Постановка множества задач в очередь на фискализацию

        :param list check: Список экземпляров чека
        :param int qid: Идентификатор очереди
        """
        qid = self.__handle_queue_id(qid)
        rep = self.__post('/api/shop/v2/queues/%s/multi-tasks' % qid,
                          [dict(check) for check in checks])
        rep.raise_for_status()
        result = rep.json()
        return [Task(**value) for value in result.values()]

    def get_task_info(self, task_id):
        """
        Возвращает информацию о поставленной на фискализацию задаче

        :param str|int task_id: ID задачи
        """
        rep = self.__get('/api/shop/v2/tasks/%s' % task_id)
        rep.raise_for_status()
        result = rep.json()
        return TaskInfo(**result)

    def get_orders(self, start='0', limit='10', courier_id=None, date_start=None,):
        """
        Возвращает информацию о заказах
        :param string courier_id: Индетификатор курьера
        :param string date_start: Дата и время доставки (с)
        :param string start: Начинать вывод заказов с start
        :param string limit: Ограничить вывод заказов на limit элементов
        """

        url = '/api/shop/v2/orders?start=%s&limit=%s' % (start, limit)
        if courier_id:
            url += '&courier_id=%s' % courier_id

        if date_start:
            url += '&date_start=%s' % date_start

        rep = self.__get(url)
        rep.raise_for_status()
        result = rep.json()
        return result

    def create_order(self, order):
        """
        Создание заказа на доставку

        :param Order order: Экземпляр заказа
        """
        rep = self.__post('/api/shop/v2/orders', dict(order))
        rep.raise_for_status()
        result = rep.json()
        return OrderInfo(**result)

    def update_order(self, oid, order):
        """
        Обновление заказа на доставку
        :param int oid: Идентификатор заказа
        :param Order order: Экземпляр заказа
        """
        rep = self.__put('/api/shop/v2/orders/%s' % oid, dict(order))
        rep.raise_for_status()
        result = rep.json()
        return OrderInfo(**result)

    def get_order_info(self, oid):
        """
        Просмотр информации о заказе
        :param int oid: Идентификатор заказа
        """
        rep = self.__get('/api/shop/v2/orders/%s' % oid)
        rep.raise_for_status()
        result = rep.json()
        return OrderInfo(**result)

    def delete_order(self, oid):
        """
        Удаление заказа
        :param int oid: Идентификатор заказа
        """
        rep = self.__delete('/api/shop/v2/orders/%s' % oid)
        rep.raise_for_status()
        return True

    def get_employees(self, type=None, start='0', limit='10'):
        """
        Возвращает информацию о курьерах
        :param EmployeeType type: Тип сотрудника
        :param string start: Начинать вывод сотрудников с start
        :param string limit: Ограничить вывод сотрудников на limit элементов
        """
        url = '/api/shop/v2/employees?start=%s&limit=%s' % (start, limit)
        if type:
            url += '&type=%s' % type

        rep = self.__get(url)
        rep.raise_for_status()
        result = rep.json()
        return result

    def create_employee(self, employee):
        """
        Создание сотрудника
        :param Employee employee: Экземпляр сотрудника
        """
        rep = self.__post('/api/shop/v2/employees', dict(employee))
        rep.raise_for_status()
        result = rep.json()
        return EmployeeInfo(**result)

    def update_employee(self, eid, employee):
        """
        Обновление информации о сотруднике
        :param int eid: Идентификатор сотрудника
        :param Employee employee: Экземпляр сотрудника
        """
        rep = self.__put('/api/shop/v2/employees/%s' % eid, dict(employee))
        rep.raise_for_status()
        result = rep.json()
        return EmployeeInfo(**result)

    def get_employee_info(self, eid):
        """
        Просмотр информации о сотруднике
        :param int eid: Идентификатор сотрудника
        """
        rep = self.__get('/api/shop/v2/employees/%s' % eid)
        rep.raise_for_status()
        result = rep.json()
        return EmployeeInfo(**result)

    def delete_employee(self, eid):
        """
        Удаление сотрудника
        :param int eid: Идентификатор сотрудника
        """
        rep = self.__delete('/api/shop/v2/employees/%s' % eid)
        rep.raise_for_status()
        return True

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

    def __put(self, path, data):
        url = self.__get_url(path)
        data = json_encode(data)
        headers = {
            'Authorization': self.__shop_id,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-HMAC-Signature': self.__get_signature('PUT', url, data)
        }
        return requests.put(url=url, headers=headers, data=data)

    def __delete(self, path):
        url = self.__get_url(path)
        headers = {
            'Authorization': self.__shop_id,
            'Accept': 'application/json',
            'X-HMAC-Signature': self.__get_signature('DELETE', url)
        }
        return requests.delete(url=url, headers=headers, allow_redirects=True)
