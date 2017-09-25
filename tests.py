# -*- coding: utf-8 -*-
from decimal import Decimal
from unittest import TestCase

from mock import patch

from komtet_kassa_sdk import (
    Check, CorrectionCheck, Client, Intent, Task, TaxSystem, VatRate, CorrectionType
)


class TestVatRate(TestCase):
    def test_parse(self):
        for src, dest in [
            ('no', 'no'),
            (0, '0'),
            ('0', '0'),
            (10, '10'),
            (10.0, '10'),
            ('10%', '10'),
            (0.18, '18'),
            ('0.18', '18'),
            ('110', '110'),
            ('118', '118'),
            ('10/110', '110'),
            ('18/118', '118')
        ]:
            self.assertEqual(VatRate.parse(src), dest)

        with self.assertRaises(ValueError) as ctx:
            VatRate.parse('unknown')
        self.assertEqual(ctx.exception.args, ('Unknown VAT rate: unknown',))


class TestCheck(TestCase):
    def test_check(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.add_payment(100)
        check.add_position('name 0', price=100)
        check.add_payment(200)
        check.add_position('name 1', 100, quantity=2, measure_name='kg')
        check.add_payment(300)
        check.add_position('name 2', 100, 3, total=290, vat=18)

        expected = {
            'task_id': 1,
            'user': 'user@host',
            'print': False,
            'intent': 'sell',
            'sno': 0,
            'payments': [
                {'sum': 100, 'type': 'card'},
                {'sum': 200, 'type': 'card'},
                {'sum': 300, 'type': 'card'},
            ],
            'positions': [
                {
                    'name': 'name 0',
                    'price': 100,
                    'quantity': 1,
                    'total': 100,
                    'vat': 'no'
                },
                {
                    'name': 'name 1',
                    'price': 100,
                    'quantity': 2,
                    'total': 200,
                    'vat': 'no',
                    'measure_name': 'kg'
                },
                {
                    'name': 'name 2',
                    'price': 100,
                    'quantity': 3,
                    'total': 290,
                    'vat': '18'
                }
            ]
        }
        for key, value in check:
            self.assertEqual(expected[key], value)

        check.set_print(True)
        self.assertTrue(check['print'])
        check.set_print(False)
        self.assertFalse(check['print'])


class TestCorrectionCheck(TestCase):
    def test_check(self):
        check = CorrectionCheck(2, '00112233445566', Intent.SELL_CORRECTION, TaxSystem.COMMON)
        check.set_payment(10, VatRate.RATE_10)
        check.set_correction_data(CorrectionType.FORCED, '2017-09-28', 'K11',
                                  'Отключение электричества')

        expected = {
            'task_id': 2,
            'printer_number': '00112233445566',
            'intent': 'sellCorrection',
            'sno': 0,
            'payments': [
                {'sum': 10, 'type': 'card'},
            ],
            'positions': [
                {
                    'name': 'Коррекция прихода',
                    'price': 10,
                    'quantity': 1,
                    'total': 10,
                    'vat': '10'
                }
            ],
            'correction': {
                'type': 'forced',
                'date': '2017-09-28',
                'document': 'K11',
                'description': 'Отключение электричества'
            }
        }
        for key, value in check:
            self.assertEqual(expected[key], value)

        self.assertEqual(check['printer_number'], '00112233445566')


class ResponseMock(object):
    def __init__(self, **kwargs):
        self.data = kwargs

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


class TestClient(TestCase):
    def setUp(self):
        self.client = Client('shop-id', 'secret-key')

    def test_is_queue_active(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
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
        with patch('komtet_kassa_sdk.client.requests') as requests:
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
