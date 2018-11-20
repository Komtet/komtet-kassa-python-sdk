# -*- coding: utf-8 -*-
from decimal import Decimal
from unittest import TestCase

from komtet_kassa_sdk import (Agent, AgentType, CalculationMethod, CalculationSubject, Check,
                              Client, CorrectionCheck, CorrectionType, Intent, Task, TaskInfo,
                              TaxSystem, VatRate)
from mock import patch


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
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON, payment_address='ул.Мира')
        check.add_payment(100)
        check.add_position('name 0', price=100, oid=1)
        check.add_payment(200)
        check.add_position('name 1', 100, quantity=2, measure_name='kg', oid='2')
        check.add_payment(300)
        check.add_position('name 2', 100, 3, total=290, vat=18)
        check.set_callback_url('http://test.pro')

        expected = {
            'task_id': 1,
            'user': 'user@host',
            'print': False,
            'intent': 'sell',
            'sno': 0,
            'payment_address': 'ул.Мира',
            'payments': [
                {'sum': 100, 'type': 'card'},
                {'sum': 200, 'type': 'card'},
                {'sum': 300, 'type': 'card'},
            ],
            'positions': [
                {
                    'id': 1,
                    'name': 'name 0',
                    'price': 100,
                    'quantity': 1,
                    'total': 100,
                    'vat': 'no'
                },
                {
                    'id': '2',
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
            ],
            'callback_url': 'http://test.pro'
        }
        for key, value in check:
            self.assertEqual(expected[key], value)

        check.set_print(True)
        self.assertTrue(check['print'])
        check.set_print(False)
        self.assertFalse(check['print'])

    def test_check_ffd_105(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.add_payment(100)
        check.add_cashier('Иваров И.П.', '1234567890123')

        agent = Agent(AgentType.COMMISSIONAIRE, "+77777777777", "ООО 'Лютик'", "12345678901")
        self.assertEqual(agent['supplier_info']['inn'], '12345678901')

        check.add_position('name 0', price=100, oid=1,
                           calculation_method=CalculationMethod.FULL_PAYMENT,
                           calculation_subject=CalculationSubject.PRODUCT,
                           agent=agent)
        check.add_payment(200)
        check.add_position('name 1', 100, quantity=2, measure_name='kg', oid='2')
        check.add_payment(300)
        check.add_position('name 2', 100, 3, total=290, vat=18)

        expected = {
            'task_id': 1,
            'user': 'user@host',
            'print': False,
            'intent': 'sell',
            'sno': 0,
            'cashier': {
                'name': 'Иваров И.П.',
                'inn': '1234567890123'
            },
            'payments': [
                {'sum': 100, 'type': 'card'},
                {'sum': 200, 'type': 'card'},
                {'sum': 300, 'type': 'card'}
            ],
            'positions': [
                {
                    'id': 1,
                    'name': 'name 0',
                    'price': 100,
                    'quantity': 1,
                    'total': 100,
                    'vat': 'no',
                    'calculation_method': 'full_payment',
                    'calculation_subject': 'product',
                    'agent_info': {
                        'type': 'commissionaire'
                    },
                    'supplier_info': {
                        'phones': ["+77777777777"],
                        'name': "ООО 'Лютик'",
                        'inn': "12345678901"
                    }
                },
                {
                    'id': '2',
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
        check.set_authorised_person('Иванов И.И.', '123456789012')
        check.set_callback_url('http://test.pro')

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
            },
            'authorised_person': {
                'name': 'Иванов И.И.',
                'inn': '123456789012'
            },
            'callback_url': 'http://test.pro'
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

    def test_get_task_info_success(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
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


class TestAgent(TestCase):
    def setUp(self):
        self.agent = Agent(AgentType.PAYMENT_AGENT, "+87776665544", "ООО 'Лютик'", "12345678901")

    def test_simple_agent(self):

        expected = {
            "agent_info": {
                "type": "payment_agent",
            },
            "supplier_info": {
                "phones": ["+87776665544"],
                "name": "ООО 'Лютик'",
                "inn": "12345678901"
            }
        }
        self.assertEqual(dict(self.agent), expected)

    def test_paying_agent(self):
        self.agent.set_paying_agent_info('Оплата', ['+87654443322'])

        expected = {
            "agent_info": {
                "type": "payment_agent",
                "paying_agent": {
                    "operation": "Оплата",
                    "phones": ["+87654443322"]
                }
            },
            "supplier_info": {
                "phones": ["+87776665544"],
                "name": "ООО 'Лютик'",
                "inn": "12345678901"
            }
        }
        self.assertEqual(dict(self.agent), expected)

    def test_receive_payments_operator(self):
        self.agent.set_receive_payments_operator_info(['+87654443322'])

        expected = {
            "agent_info": {
                "type": "payment_agent",
                "receive_payments_operator": {
                    "phones": ["+87654443322"]
                }
            },
            "supplier_info": {
                "phones": ["+87776665544"],
                "name": "ООО 'Лютик'",
                "inn": "12345678901"
            }
        }
        self.assertEqual(dict(self.agent), expected)

    def test_money_transfer_operator(self):
        self.agent.set_money_transfer_operator_info(
            'Оператор', ['+87654443322'], 'ул.Мира', '0123456789')

        expected = {
            "agent_info": {
                "type": "payment_agent",
                "money_transfer_operator": {
                    "name": "Оператор",
                    "phones": ["+87654443322"],
                    "address": "ул.Мира",
                    "inn": "0123456789"
                }
            },
            "supplier_info": {
                "phones": ["+87776665544"],
                "name": "ООО 'Лютик'",
                "inn": "12345678901"
            }
        }
        self.assertEqual(dict(self.agent), expected)
