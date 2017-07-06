import decimal
import json

from collections import OrderedDict
from unittest import TestCase

import six

from komtet_kassa_sdk import configure, PrintQueue, Check, VAT0
from komtet_kassa_sdk.exc import CheckError, FormatError
from komtet_kassa_sdk.utils import asbool, JSONEncoder


def configure_package():
    configure({
        'shop_key': 'YoUr_sHOp_Key',
        'shop_secret': 'yoUR_sHop_SecReT',
        'server': 'http://test.online-kassa.com',
        'path_prefix': '/api/shop/v1',
        'sno': 2,
        'named_queues': {
            '__default__': 123,
            'first_queue': 123,
            'second_queue': 231,
            'third_queue': 312
        }
    })


class TestQueue(TestCase):

    def setUp(self):
        configure_package()

    def test_configure(self):
        PrintQueue.configure('''{
            "shop_key": "YoUr_sHOp_Key",
            "shop_secret": "yoUR_sHop_SecReT",
            "server": "http://test.online-kassa.com",
            "path_prefix": "/api/shop/v1",
            "named_queues": {
                "__default__": 123,
                "first_queue": 123,
                "second_queue": 231,
                "third_queue": 312
            }
        }''')
        self.assertEqual(OrderedDict(PrintQueue.__queues__),
                         OrderedDict({
            'shop_key': 'YoUr_sHOp_Key',
            'shop_secret': 'yoUR_sHop_SecReT',
            'server': 'http://test.online-kassa.com',
            'path_prefix': '/api/shop/v1',
            'named_queues': {
                '__default__': 123,
                'first_queue': 123,
                'second_queue': 231,
                'third_queue': 312
            }
        }))

    def test_named_queues(self):
        self.assertEqual(PrintQueue().id, 123)
        self.assertEqual(PrintQueue('second_queue').id, 231)
        self.assertEqual(PrintQueue(312).id, 312)


class TestCheck(TestCase):

    def setUp(self):
        configure_package()

    def test_create_success(self):
        check = Check(
            task_id='t00123',
            positions=[{
                'name': 'banana',
                'price': 150
            }, {
                'name': 'milk',
                'price': 152.5,
                'quantity': 2
            }],
            payment=455,
            user_email='user_email_to_send_check@mail.ru'
        )

        check._validate()

    def test_create_failed_with_error_in_position(self):
        check = Check(
            task_id='t00123',
            positions=[{
                'name': 'banana',
                'price': 150,
                'total': 200
            }, {
                'name': 'milk',
                'price': 152.5,
                'quantity': 2
            }],
            payments=[455],
            user_email='user_email_to_send_check@mail.ru'
        )

        self.assertRaises(CheckError, check._validate)

    def test_create_failed_with_invalid_position(self):
        check = Check(task_id='t00123', user_email='user@mail.ru')
        self.assertRaises(FormatError, check.append_position, {})

    def test_create_failed_with_invalid_payment(self):
        check = Check(task_id='t00123', user_email='user@mail.ru')
        self.assertRaises(FormatError, check.append_payment, {})

    def test_prepare(self):
        check = Check(
            task_id='t00123',
            positions=[{
                'name': 'banana',
                'price': 150,
                'vat': {
                    'number': VAT0,
                    'sum': 0
                }
            }, {
                'name': 'milk',
                'price': 152.5,
                'quantity': 2,
                'discount': 123
            }],
            payment=450,
            user_email='user_email_to_send_check@mail.ru',
        )

        self.assertIn('total', check._prepare()['positions'][0])


class TestUtils(TestCase):

    def test_asbool(self):
        self.assertTrue(asbool(u'yes'))
        self.assertFalse(asbool('off'))
        self.assertRaises(ValueError, asbool, 'ololo')
        self.assertTrue(asbool(1))

    def test_json_encoder(self):
        self.assertEqual(json.dumps(decimal.Decimal(123.3), cls=JSONEncoder), '123.3')
        self.assertRaises(TypeError, json.dumps, decimal.Decimal(123.3))
