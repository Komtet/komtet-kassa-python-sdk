# -*- coding: utf-8 -*-
from decimal import Decimal
from unittest import TestCase

from komtet_kassa_sdk.v1 import (Client, EmployeeType, Task, TaskInfo)
from ...helpers.mock import ResponseMock
from mock import patch


class TestClient(TestCase):
    def setUp(self):
        self.client = Client('shop-id', 'secret-key')

    def test_is_queue_active(self):
        with patch('komtet_kassa_sdk.v1.client.requests') as requests:
            requests.get.return_value = ResponseMock(state='active')
            self.assertTrue(self.client.is_queue_active(1))
            requests.get.assert_called_with(
                allow_redirects=True,
                headers={
                    'Authorization': 'shop-id',
                    'Accept': 'application/json',
                    'X-HMAC-Signature': 'b72f98703ccaea912cdf06e364d81885'
                },
                url='https://kassa.komtet.ru/api/shop/v1/queues/1'
            )

            self.assertIs(self.client, self.client.set_host('new-host'))
            requests.get.return_value = ResponseMock(state='passive')
            self.assertFalse(self.client.is_queue_active(1))
            requests.get.assert_called_with(
                allow_redirects=True,
                headers={
                    'Authorization': 'shop-id',
                    'Accept': 'application/json',
                    'X-HMAC-Signature': 'd7f30739a1cf280291f763d80d6d5bfd'
                },
                url='new-host/api/shop/v1/queues/1'
            )

            with self.assertRaises(ValueError) as ctx:
                self.client.is_queue_active()
            self.assertEqual(ctx.exception.args, ('Queue ID is not specified',))

            self.client.set_default_queue(2)
            self.assertFalse(self.client.is_queue_active())
            requests.get.assert_called_with(
                allow_redirects=True,
                headers={
                    'Authorization': 'shop-id',
                    'Accept': 'application/json',
                    'X-HMAC-Signature': '000ed801dae724e047bc74b67743af1d'
                },
                url='new-host/api/shop/v1/queues/2'
            )

    def test_create_task_success(self):
        with patch('komtet_kassa_sdk.v1.client.requests') as requests:
            response_mock = ResponseMock(id=1, external_id=2, print_queue_id=3, state='new')
            requests.post.return_value = response_mock
            task = self.client.create_task({'key': Decimal('10.0')}, 3)
            self.assertIsInstance(task, Task)
            self.assertEqual(task.id, 1)
            self.assertEqual(task.external_id, 2)
            self.assertEqual(task.print_queue_id, 3)
            self.assertEqual(task.state, 'new')
            requests.post.assert_called_with(
                headers={
                    'Authorization': 'shop-id',
                    'Accept': 'application/json',
                    'X-HMAC-Signature': '5bfe6ef2290053624fdda725177caa33',
                    'Content-Type': 'application/json'
                },
                url='https://kassa.komtet.ru/api/shop/v1/queues/3/task',
                data='{"key": 10.0}'
            )

            with self.assertRaises(ValueError) as ctx:
                self.client.create_task({'key': 'value'})
            self.assertEqual(ctx.exception.args, ('Queue ID is not specified',))

            self.client.set_default_queue(2)
            with self.assertRaises(TypeError) as ctx:
                self.client.create_task({'key': object()})
            self.assertIn('is not JSON serializable', ctx.exception.args[0])

    def test_get_task_info_success(self):
        with patch('komtet_kassa_sdk.v1.client.requests') as requests:
            response_mock = ResponseMock(
                id=234, external_id='4321', state='done', error_description=None,
                fiscal_data={
                    'i': '111',
                    'fn': '2222222222222222',
                    't': '3333333333333',
                    'n': 4,
                    'fp': '555555555',
                    's': '6666.77'
                })
            requests.get.return_value = response_mock
            task_info = self.client.get_task_info(234)
            self.assertIsInstance(task_info, TaskInfo)
            self.assertEqual(task_info.id, 234)
            self.assertEqual(task_info.external_id, '4321')
            self.assertEqual(task_info.state, 'done')
            self.assertIsNone(task_info.error_description)
            self.assertDictEqual(task_info.fiscal_data, {
                'i': '111',
                'fn': '2222222222222222',
                't': '3333333333333',
                'n': 4,
                'fp': '555555555',
                's': '6666.77'
            })

    def test_get_couriers_success(self):
        with patch('komtet_kassa_sdk.v1.client.requests') as requests:
            response_mock = ResponseMock(
                account_employees=[
                    {
                        'email': 'q@mail.ru',
                        'id': 46,
                        'phone': '1',
                        'name': 'Dima D'
                    },
                    {
                        'email': 'q@q.com',
                        'id': 57,
                        'phone': '1',
                        'name': 'qwerty'
                    },
                    {
                        'email': 'ivanov@example.com',
                        'id': 2,
                        'phone': '+70000000000',
                        'name': 'Иванов И.П.'
                    }],
                meta={'total': 3, 'total_pages': 1}
            )
            requests.get.return_value = response_mock
            couriers_info = self.client.get_employees(type=EmployeeType.COURIER)
            self.assertDictEqual(couriers_info['meta'], {'total': 3, 'total_pages': 1})
            self.assertDictEqual(couriers_info['account_employees'][0], {
                'email': 'q@mail.ru',
                'id': 46,
                'phone': '1',
                'name': 'Dima D'
            })
            self.assertDictEqual(couriers_info['account_employees'][1], {
                'email': 'q@q.com',
                'id': 57,
                'phone': '1',
                'name': 'qwerty'
            })
            self.assertDictEqual(couriers_info['account_employees'][2], {
                'email': 'ivanov@example.com',
                'id': 2,
                'phone': '+70000000000',
                'name': 'Иванов И.П.'
            })
