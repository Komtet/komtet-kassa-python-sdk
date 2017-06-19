import json

import six

from requests import ConnectionError

from . import request, exc, constants as c


class PrintQueue(object):

    @classmethod
    def configure(cls, named_queues=None):
        if isinstance(named_queues, dict):
            cls.__queues__ = named_queues
        else:
            cls.__queues__ = json.loads(named_queues or '{}')

    def __init__(self, id_=None):
        if not id_:
            self.id = self.__queues__['__default__']
        elif isinstance(id_, six.string_types):
            self.id = self.__queues__[id_]
        else:
            self.id = id_

    def is_ready(self):
        return self.get_state() == c.ACTIVE_QUEUE_STATE

    def get_state(self):
        try:
            res = request.get('/queues/{}'.format(self.id))
        except ConnectionError:
            return c.PASSIVE_QUEUE_STATE

        if res.status_code == 200:
            return res.json()['state']

        return c.PASSIVE_QUEUE_STATE

    def put_task(self, task, shop_key=None, shop_secret=None):
        res = request.post('/queues/{}/task'.format(self.id), json=task,
                           shop_key=shop_key, shop_secret=shop_secret)

        if res.status_code in [401, 403]:
            raise exc.ServerError(res.json()['title'], res.status_code)
        elif res.status_code == 422:
            error = res.json()
            raise exc.TaskError(error['title'], error['description'])
        if res.status_code != 200:
            raise exc.ServerError('Server not respond', res.status_code)

        return res.json()
