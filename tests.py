# -*- coding: utf-8 -*-
from decimal import Decimal
from unittest import TestCase

from komtet_kassa_sdk import (Agent, AgentType, CalculationMethod, CalculationSubject, Check,
                              Client, CorrectionCheck, CorrectionType, Employee, EmployeeInfo,
                              EmployeeType, Intent, Nomenclature, Order, OrderInfo, PaymentMethod,
                              Task, TaskInfo, TaxSystem, VatRate)
from komtet_kassa_sdk.client import Response
from komtet_kassa_sdk.lib.helpers import correction_positions
from mock import patch


class TestVatRate(TestCase):
    def test_parse(self):
        for src, dest in [
            ('no', 'no'),
            (0, '0'),
            (0.18, '20'),
            (0.2, '20'),
            (0.20, '20'),
            (10, '10'),
            (10.0, '10'),
            (18, '20'),
            (20, '20'),
            (20.0, '20'),
            ('10%', '10'),
            ('18%', '20'),
            ('20%', '20'),
            ('0', '0'),
            ('0.18', '20'),
            ('0.20', '20'),
            ('110', '110'),
            ('118', '120'),
            ('10/110', '110'),
            ('18/118', '120'),
            ('20/120', '120')
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
        check.add_position('name 2', 100, 3, total=290, vat=20)
        check.set_callback_url('http://test.pro')

        expected = {
            'external_id': 1,
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
                    'vat': '20'
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

    def test_check_ffd_105_with_client_name(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_client(name='Иванов И.П.')

        self.assertEqual(check._Check__data['client']['name'], 'Иванов И.П.')

    def test_check_ffd_105_with_client_inn(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_client(inn='1231231231')

        self.assertEqual(check._Check__data['client']['inn'], '1231231231')

    def test_check_ffd_105_with_empty_client(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_client()

        self.assertEqual(check._Check__data.get('client'), None)

    def test_check_ffd_105(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_client(name='Иванов И.П.', inn='1231231231')
        check.set_cashier('Иваров И.П.', '1234567890123')
        check.add_payment(100)

        agent = Agent(AgentType.COMMISSIONAIRE, "+77777777777", "ООО 'Лютик'", "12345678901")
        self.assertEqual(agent['supplier_info']['inn'], '12345678901')

        nomenclature = Nomenclature()
        nomenclature.code = '019876543210123421sgEKKPPcS25y5'
        check.add_position('name 0', price=100, oid=1,
                           calculation_method=CalculationMethod.FULL_PAYMENT,
                           calculation_subject=CalculationSubject.PRODUCT,
                           agent=agent, nomenclature=nomenclature, excise=19.89,
                           country_code='643', declaration_number='10129000/220817/0211234')

        nomenclature = Nomenclature()
        nomenclature.code = '019876543210123421sgEKKPPcS25y5'
        nomenclature.hex_code = '444D00000096b43f303132333432317367454b4b5050635332357935'
        check.add_position('name 1', 100, quantity=2, measure_name='kg', oid='2',
                           nomenclature=nomenclature)

        nomenclature = Nomenclature()
        nomenclature.hex_code = '444D00000096b43f303132333432317367454b4b5050635332357935'
        check.add_position('name 2', 100, 3, total=290, vat=20, nomenclature=nomenclature)

        check.add_payment(200)
        check.add_payment(300)

        expected = {
            'external_id': 1,
            'user': 'user@host',
            'print': False,
            'intent': 'sell',
            'sno': 0,
            'cashier': {
                'name': 'Иваров И.П.',
                'inn': '1234567890123'
            },
            'client': {
                'name': 'Иванов И.П.',
                'inn': '1231231231'
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
                    'excise': 19.89,
                    'country_code': '643',
                    'declaration_number': '10129000/220817/0211234',
                    'agent_info': {
                        'type': 'commissionaire'
                    },
                    'supplier_info': {
                        'phones': ["+77777777777"],
                        'name': "ООО 'Лютик'",
                        'inn': "12345678901"
                    },
                    'nomenclature_code': {
                        'code': '019876543210123421sgEKKPPcS25y5'
                    }
                },
                {
                    'id': '2',
                    'name': 'name 1',
                    'price': 100,
                    'quantity': 2,
                    'total': 200,
                    'vat': 'no',
                    'measure_name': 'kg',
                    'nomenclature_code': {
                        'code': '019876543210123421sgEKKPPcS25y5',
                        'hex_code': '444D00000096b43f303132333432317367454b4b5050635332357935'
                    }
                },
                {
                    'name': 'name 2',
                    'price': 100,
                    'quantity': 3,
                    'total': 290,
                    'vat': '20',
                    'nomenclature_code': {
                        'hex_code': '444D00000096b43f303132333432317367454b4b5050635332357935'
                    }
                }
            ]
        }
        for key, value in check:
            self.assertEqual(expected[key], value)

        check.set_print(True)
        self.assertTrue(check['print'])
        check.set_print(False)
        self.assertFalse(check['print'])

    def test_set_additional_check_props(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_additional_check_props('Дополнительный реквизит чека')
        self.assertEqual(check['additional_check_props'], 'Дополнительный реквизит чека')

    def test_set_additional_user_props(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_additional_user_props('Наименование', 'Значение')
        self.assertEqual(check['additional_user_props'],
                         {'name': 'Наименование', 'value': 'Значение'})

    def test_apply_discount(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_client(name='Иванов И.П.', inn='1231231231')
        check.set_cashier('Иваров И.П.', '1234567890123')
        check.add_position('name 0', price=120.67, oid=1,
                           calculation_method=CalculationMethod.FULL_PAYMENT,
                           calculation_subject=CalculationSubject.PRODUCT)
        check.add_position('name 1', price=113.54, oid=2,
                           calculation_method=CalculationMethod.FULL_PAYMENT,
                           calculation_subject=CalculationSubject.PRODUCT)
        check.apply_discount(50)

        self.assertEqual(check['positions'][0]['total'], Decimal('94.91'))
        self.assertEqual(check['positions'][1]['total'], Decimal('89.30'))

    def test_apply_correction_positions(self):
        '''
        Тест применения алгоритма корректировки позиции
        '''

        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.add_position(oid=1, name='Позиция 1', price=Decimal('42.4'),
                           quantity=2, total=Decimal(84.5))

        check.add_position(oid='2', name="Доставка", price=10)
        check.apply_correction_positions()
        self.assertEqual(len(check['positions']), 3)


class TestCorrectionCheck(TestCase):
    def test_check(self):
        check = CorrectionCheck(2, '00112233445566', Intent.SELL_CORRECTION, TaxSystem.COMMON)
        check.set_payment(10, VatRate.RATE_10)
        check.set_correction_data(CorrectionType.FORCED, '2017-09-28', 'K11',
                                  'Отключение электричества')
        check.set_authorised_person('Иванов И.И.', '123456789012')
        check.set_callback_url('http://test.pro')

        expected = {
            'external_id': 2,
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


class ResponseListMock(object):
    def __init__(self, data):
        self.data = data

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

    def test_get_couriers_success(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
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


class TestOrder(TestCase):
    def test_order(self):
        self.maxDiff = None
        order = Order(order_id='123', state='new', sno=0)

        order.set_client(name='Сергеев Виктор Сергеевич',
                         address='г.Пенза, ул.Суворова д.10 кв.25',
                         phone='+87654443322',
                         email='client@email.com')
        order.set_delivery_time(date_start="2018-02-28 14:00",
                                date_end="2018-02-28 15:20")
        order.set_description('Комментарий к заказу')
        order.add_position(oid='1', type='product', name='position name1', price=555.0)
        order.add_position(oid='2', type='product', name='position name2', price=100.0,
                           quantity=5, vat=VatRate.RATE_10, measure_name='kg')
        order.add_position(oid='3', type='product', name='position name3', price=555.0,
                           excise=19.89, country_code='643',
                           declaration_number='10129000/220817/0211234')

        expected = {
            "order_id": '123',
            "client_name": "Сергеев Виктор Сергеевич",
            "client_address": "г.Пенза, ул.Суворова д.10 кв.25",
            "client_phone": "+87654443322",
            "client_email": "client@email.com",
            "is_paid": False,
            "prepayment": 0,
            "payment_type": PaymentMethod.CARD,
            "description": "Комментарий к заказу",
            "state": "new",
            "date_start": "2018-02-28 14:00",
            "date_end": "2018-02-28 15:20",
            "items": [
                {
                    "order_item_id": '1',
                    "type": "product",
                    "name": "position name1",
                    "price": 555.0,
                    "quantity": 1,
                    "total": 555.0,
                    "vat": "no",
                },
                {
                    "order_item_id": '2',
                    "type": "product",
                    "name": "position name2",
                    "price": 100.0,
                    "quantity": 5,
                    "total": 500.0,
                    "vat": "10",
                    "measure_name": "kg"
                },
                {
                    "order_item_id": '3',
                    "type": "product",
                    "name": "position name3",
                    "price": 555.0,
                    "quantity": 1,
                    "total": 555.0,
                    "vat": "no",
                    "excise": 19.89,
                    "country_code": '643',
                    "declaration_number": "10129000/220817/0211234"
                }
            ],
            "sno": 0,
            "courier_id": ''
        }
        for key, value in order:
            self.assertEqual(expected[key], value)

    def test_order_with_callback_url(self):
        self.maxDiff = None
        order = Order(order_id='123', state='new', sno=0)

        order.set_client(name='Сергеев Виктор Сергеевич',
                         address='г.Пенза, ул.Суворова д.10 кв.25',
                         phone='+87654443322',
                         email='client@email.com')
        order.set_delivery_time(date_start="2018-02-28 14:00",
                                date_end="2018-02-28 15:20")
        order.set_description('Комментарий к заказу')
        order.add_position(oid='1', type='product', name='position name1', price=555.0)
        order.add_position(oid='2', type='product', name='position name2', price=100.0,
                           quantity=5, vat=VatRate.RATE_10, measure_name='kg')

        order.add_callback_url('https://callback_url.ru')
        order.add_courier_id(1)

        expected = {
            "order_id": '123',
            "client_name": "Сергеев Виктор Сергеевич",
            "client_address": "г.Пенза, ул.Суворова д.10 кв.25",
            "client_phone": "+87654443322",
            "client_email": "client@email.com",
            "is_paid": False,
            "prepayment": 0,
            "payment_type": PaymentMethod.CARD,
            "description": "Комментарий к заказу",
            "state": "new",
            "date_start": "2018-02-28 14:00",
            "date_end": "2018-02-28 15:20",
            "items": [
                {
                    "order_item_id": '1',
                    "type": "product",
                    "name": "position name1",
                    "price": 555.0,
                    "quantity": 1,
                    "total": 555.0,
                    "vat": "no",
                },
                {
                    "order_item_id": '2',
                    "type": "product",
                    "name": "position name2",
                    "price": 100.0,
                    "quantity": 5,
                    "total": 500.0,
                    "vat": "10",
                    "measure_name": "kg"
                }
            ],
            "sno": 0,
            "courier_id": 1,
            "callback_url": 'https://callback_url.ru'
        }
        for key, value in order:
            self.assertEqual(expected[key], value)

    def test_apply_discount(self):
        order = Order(order_id='123', state='new', sno=0)
        order.add_position(oid='1', type='product', name='position name1', price=120.67)
        order.add_position(oid='2', type='product', name='position name2', price=113.54)
        order.apply_discount(50)

        self.assertEqual(order['items'][0]['total'], Decimal('94.91'))
        self.assertEqual(order['items'][1]['total'], Decimal('89.30'))

    def test_position_add_nomenclature_code(self):
        order = Order(order_id='123', state='new', sno=0)
        order.add_position(oid='1', type='product', name='position name1', price=120.67,
                           nomenclature_code='019876543210123421sgEKKPPcS25y5',
                           is_need_nomenclature_code=False)

        self.assertEqual(order['items'][0]['nomenclature_code'], '019876543210123421sgEKKPPcS25y5')
        self.assertFalse(order['items'][0]['is_need_nomenclature_code'])

    def test_add_client_longitude_latitude(self):
        order = Order(order_id='123', state='new', sno=0)
        order.add_position(oid='1', type='product', name='test position1', price=1990)
        order.set_client(name='Иванов Иван Петрович',
                         address='г.Пенза, ул.Суворова д.144а',
                         phone='+79273784183',
                         email='client@email.com',
                         latitude='53.202838856701206',
                         longitude='44.99768890421866')

        self.assertEqual(order._Order__data['client_address_latitude'], '53.202838856701206')
        self.assertEqual(order._Order__data['client_address_longitude'], '44.99768890421866')


class TestClientOrder(TestCase):
    def setUp(self):
        self.client = Client('shop-id', 'secret-key')
        self.response_mock = ResponseMock(
            id=775, client_name='test test test', client_address='обл Пензенская, Пенза',
            client_email='', client_phone='88005553535', sno=0, is_paid=True,
            payment_type='cash', description='', state='new',
            items=[
                {
                    'name': 'Демо-товар 2',
                    'measure_name': None,
                    'quantity': 5.0,
                    'total': 7500.0,
                    'vat': '10',
                    'external_id': '1',
                    'id': 3590,
                    'price': 1500.0
                },
                {
                    'name': 'Доставка',
                    'measure_name': None,
                    'quantity': 1.0,
                    'total': 500.0,
                    'vat': 'no',
                    'external_id': '2',
                    'id': 3591,
                    'price': 500.0
                }
            ],
            amount=2000.0, prepayment=200.0, courier=None, is_pay_to_courier=False,
            date_start='2019-04-12 07:00',
            date_end='2019-04-12 13:00',
            callback_url='https://calback_url.ru')

    def test_create_order_success(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
            requests.post.return_value = self.response_mock

            order = Order(order_id=2589, is_paid=True, state='new', sno=0)

            order.set_client(name='test test test',
                             address='обл Пензенская, Пенза',
                             phone='88005553535')
            order.set_delivery_time(date_start='2019-04-12 07:00',
                                    date_end='2019-04-12 13:00')
            order.add_position(oid='1', type='product', name='Демо-товар 2', vat='10', quantity=5,
                               price=1500.0, total=1500.0)
            order.add_position(oid='2', type='delivery', name="Доставка", price=500)

            order_info = self.client.create_order(order)
            self.assertIsInstance(order_info, OrderInfo)
            self.assertEqual(order_info.id, 775)
            self.assertEqual(order_info.state, 'new')
            self.assertDictEqual(order_info.items[0], {
                'name': 'Демо-товар 2',
                'measure_name': None,
                'quantity': 5.0,
                'total': 7500.0,
                'vat': '10',
                'external_id': '1',
                'id': 3590,
                'price': 1500.0
            })
            self.assertDictEqual(order_info.items[1], {
                'name': 'Доставка',
                'measure_name': None,
                'quantity': 1.0,
                'total': 500.0,
                'vat': 'no',
                'external_id': '2',
                'id': 3591,
                'price': 500.0
            })

    def test_update_order_success(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
            requests.put.return_value = self.response_mock

            order = Order(order_id=2589, is_paid=True, state='new', sno=0)

            order.set_client(name='test test test',
                             address='обл Пензенская, Пенза',
                             phone='88005553535')
            order.set_delivery_time(date_start='2019-04-12 07:00',
                                    date_end='2019-04-12 13:00')
            order.add_position(oid='1', type='product', name='Демо-товар 2', vat='10', quantity=5,
                               price=1500.0, total=1500.0)
            order.add_position(oid='2', type='delivery', name="Доставка", price=500)

            order_info = self.client.update_order(775, order)
            self.assertIsInstance(order_info, OrderInfo)
            self.assertEqual(order_info.id, 775)
            self.assertEqual(order_info.state, 'new')
            self.assertEqual(order_info.amount, 2000.0)

    def test_get_order_info_success(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
            requests.get.return_value = self.response_mock
            order_info = self.client.get_order_info(775)
            self.assertIsInstance(order_info, OrderInfo)
            self.assertEqual(order_info.id, 775)
            self.assertEqual(order_info.client_name, 'test test test')
            self.assertEqual(order_info.state, 'new')
            self.assertEqual(order_info.client_phone, '88005553535')

            self.assertDictEqual(order_info.items[0], {
                'name': 'Демо-товар 2',
                'measure_name': None,
                'quantity': 5.0,
                'total': 7500.0,
                'vat': '10',
                'external_id': '1',
                'id': 3590,
                'price': 1500.0
            })
            self.assertDictEqual(order_info.items[1], {
                'name': 'Доставка',
                'measure_name': None,
                'quantity': 1.0,
                'total': 500.0,
                'vat': 'no',
                'external_id': '2',
                'id': 3591, 'price': 500.0
            })

    def test_create_order_with_callback_url_success(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
            requests.post.return_value = self.response_mock

            order = Order(order_id=2589, is_paid=True, state='new', sno=0)

            order.set_client(name='test test test',
                             address='обл Пензенская, Пенза',
                             phone='88005553535')
            order.set_delivery_time(date_start='2019-04-12 07:00',
                                    date_end='2019-04-12 13:00')
            order.add_position(oid='1', type='product', name='Демо-товар 2', vat='10', quantity=5,
                               price=1500.0, total=1500.0)
            order.add_position(oid='2', type='delivery', name="Доставка", price=500)

            order.add_callback_url('https://calback_url.ru')

            order_info = self.client.create_order(order)
            self.assertIsInstance(order_info, OrderInfo)
            self.assertEqual(order_info.id, 775)
            self.assertEqual(order_info.state, 'new')
            self.assertEqual(order_info.callback_url, 'https://calback_url.ru')

            self.assertDictEqual(order_info.items[0], {
                'name': 'Демо-товар 2',
                'measure_name': None,
                'quantity': 5.0,
                'total': 7500.0,
                'vat': '10',
                'external_id': '1',
                'id': 3590,
                'price': 1500.0
            })
            self.assertDictEqual(order_info.items[1], {
                'name': 'Доставка',
                'measure_name': None,
                'quantity': 1.0,
                'total': 500.0,
                'vat': 'no',
                'external_id': '2',
                'id': 3591,
                'price': 500.0
            })

    def test_set_payment_type_and_prepayment(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
            requests.post.return_value = self.response_mock

            order = Order(order_id=2589, is_paid=True, state='new', sno=0,
                          prepayment=200.0, payment_type=PaymentMethod.CASH)

            order_info = self.client.create_order(order)
            self.assertIsInstance(order_info, OrderInfo)

            self.assertEqual(order_info.payment_type, 'cash')
            self.assertEqual(order_info.prepayment, 200.0)

    def test_apply_correction_positions(self):
        '''
        Тест применения алгоритма корректировки позиции
        '''
        order = Order(order_id=2589, is_paid=True, state='new', sno=0)

        order.add_position(oid='1', type='product', name='Позиция 1', vat='10', quantity=2,
                           price=Decimal('42.4'), total=Decimal(84.5))
        order.add_position(oid='2', type='delivery', name="Доставка", price=10)
        order.apply_correction_positions()
        self.assertEqual(len(order['items']), 3)


class TestResponse(TestCase):

    def test_response(self):
        task = Response(id=12, uuid='978d4719-470a-409e-a6c4-574d17d3837a',
                        error_description=None)
        self.assertEqual(task.id, 12)
        self.assertEqual(task.uuid, '978d4719-470a-409e-a6c4-574d17d3837a')
        self.assertIsNone(task.error_description)
        self.assertDictEqual(task._asdict(), {
            'id': 12,
            'uuid': '978d4719-470a-409e-a6c4-574d17d3837a',
            'error_description': None
        })


class TestCheckAgent(TestCase):

    def test_agent(self):
        check = Check('test_id', 'test@example.com', Intent.SELL, TaxSystem.COMMON)

        agent = Agent(AgentType.AGENT, "77777777777")
        check.set_agent(agent)

        raw_check = dict(check)
        self.assertIn('agent_info', raw_check)
        self.assertDictEqual(raw_check['agent_info'], {"type": "agent"})
        self.assertIn('supplier_info', raw_check)
        self.assertDictEqual(raw_check['supplier_info'], {"phones": ["77777777777"]})


class TestSetCashier(TestCase):

    def test_set_cashier_with_inn_in_check(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_cashier('Иваров И.П.', '1234567890123')
        self.assertDictEqual(check['cashier'], {
            'name': 'Иваров И.П.',
            'inn': '1234567890123'
        })

    def test_set_cashier_without_inn_in_check(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_cashier('Иваров И.П.')
        self.assertDictEqual(check['cashier'], {
            'name': 'Иваров И.П.'
        })

    def test_set_cashier_with_inn_in_correction_check(self):
        check = CorrectionCheck(2, '00112233445566', Intent.SELL_CORRECTION, TaxSystem.COMMON)
        check.set_authorised_person('Иваров И.П.', '1234567890123')
        self.assertDictEqual(check['authorised_person'], {
            'name': 'Иваров И.П.',
            'inn': '1234567890123'
        })

    def test_set_cashier_without_inn_in_correction_check(self):
        check = CorrectionCheck(2, '00112233445566', Intent.SELL_CORRECTION, TaxSystem.COMMON)
        check.set_authorised_person('Иваров И.П.')
        self.assertDictEqual(check['authorised_person'], {
            'name': 'Иваров И.П.'
        })


class TestSetAgentInfoToOrder(TestCase):
    def setUp(self):
        self.client = Client('shop-id', 'secret-key')
        self.response_mock = ResponseMock(
            id=775, client_name='test test test', client_address='обл Пензенская, Пенза',
            client_email='', client_phone='88005553535', sno=0, is_paid=True,
            payment_type='cash', description='', state='new',
            items=[
                {
                    'name': 'Демо-товар 2',
                    'measure_name': None,
                    'quantity': 5.0,
                    'total': 7500.0,
                    'vat': '10',
                    'external_id': '1',
                    'id': 3590,
                    'price': 1500.0,
                    'agent_info': {
                        'type': 'commissionaire'
                    },
                    'supplier_info': {
                        'phones': ["+77777777777"],
                        'name': "ООО 'Лютик'",
                        'inn': "12345678901"
                    },
                },
                {
                    'name': 'Доставка',
                    'measure_name': None,
                    'quantity': 1.0,
                    'total': 500.0,
                    'vat': 'no',
                    'external_id': '2',
                    'id': 3591,
                    'price': 500.0
                }
            ],
            amount=2000.0, prepayment=200.0, courier=None, is_pay_to_courier=False,
            date_start='2019-04-12 07:00',
            date_end='2019-04-12 13:00',
            callback_url='https://calback_url.ru')

    def test_create_order_success(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
            requests.post.return_value = self.response_mock

            order = Order(order_id=2589, is_paid=True, state='new', sno=0)

            order.set_client(name='test test test',
                             address='обл Пензенская, Пенза',
                             phone='88005553535')
            order.set_delivery_time(date_start='2019-04-12 07:00',
                                    date_end='2019-04-12 13:00')

            agent = Agent(AgentType.COMMISSIONAIRE, "+77777777777", "ООО 'Лютик'", "12345678901")
            order.add_position(oid='1', type='product', name='Демо-товар 2', vat='10', quantity=5,
                               price=1500.0, total=1500.0, agent=agent)

            order.add_position(oid='2', type='delivery', name="Доставка", price=500)

            order_info = self.client.create_order(order)
            self.assertIsInstance(order_info, OrderInfo)
            self.assertEqual(order_info.id, 775)
            self.assertEqual(order_info.state, 'new')
            self.assertDictEqual(order_info.items[0], {
                'name': 'Демо-товар 2',
                'measure_name': None,
                'quantity': 5.0,
                'total': 7500.0,
                'vat': '10',
                'external_id': '1',
                'id': 3590,
                'price': 1500.0,
                'agent_info': {
                    'type': 'commissionaire'
                },
                'supplier_info': {
                    'phones': ["+77777777777"],
                    'name': "ООО 'Лютик'",
                    'inn': "12345678901"
                },
            })
            self.assertDictEqual(order_info.items[1], {
                'name': 'Доставка',
                'measure_name': None,
                'quantity': 1.0,
                'total': 500.0,
                'vat': 'no',
                'external_id': '2',
                'id': 3591,
                'price': 500.0
            })


class TestMultiTasks(TestCase):
    def setUp(self):
        self.client = Client('shop-id', 'secret-key')
        self.response_mock = ResponseListMock({
            idx: dict(id=idx, external_id=idx, print_queue_id=3, state='new') for idx in range(5)
        })

    def test_create_multi_tasks_success(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
            requests.post.return_value = self.response_mock
            checks = []
            for i in range(5):
                check = Check(1, 'user@host', Intent.SELL,
                              TaxSystem.COMMON, payment_address='ул.Мира')
                check.add_payment(100)
                check.add_position('name 0', price=100, oid=1)
                check.add_payment(200)
                check.add_position('name 1', 100, quantity=2, measure_name='kg', oid='2')
                check.add_payment(300)
                check.add_position('name 2', 100, 3, total=290, vat=20)
                check.set_callback_url('http://test.pro')

                checks.append(check)

            checks_info = self.client.create_tasks(checks, 2)
            self.assertIsInstance(checks_info, list)

            for idx, check_info in enumerate(checks_info):
                self.assertIsInstance(check_info, TaskInfo)
                expected = dict(id=idx, external_id=idx, print_queue_id=3, state='new')
                for key, value in expected.items():
                    self.assertEqual(value, getattr(check_info, key))


class TestEmployee(TestCase):
    def setUp(self):
        self.client = Client('shop-id', 'secret-key')
        self.response_mock = ResponseMock(
            id=1, name='Ivanov Ivan Ivanovich', login='test_login',
            password='test_password', pos_id='POS_KEY')

    def test_create_order_success(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
            requests.post.return_value = self.response_mock

            employee = Employee(type=EmployeeType.CASHIER, name='Ivanov Ivan Ivanovich',
                                login='test_login', password='test_password', pos_id='POS_KEY')

            employee_info = self.client.create_employee(employee)
            self.assertIsInstance(employee_info, EmployeeInfo)
            self.assertEqual(employee_info.id, 1)
            self.assertEqual(employee_info.name, 'Ivanov Ivan Ivanovich')
            self.assertEqual(employee_info.login, 'test_login')
            self.assertEqual(employee_info.password, 'test_password')
            self.assertEqual(employee_info.pos_id, 'POS_KEY')

    def test_update_order_success(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
            requests.put.return_value = self.response_mock

            employee = Employee(type=EmployeeType.CASHIER, name='Ivanov Ivan Ivanovich',
                                login='test_login', password='test_password', pos_id='POS_KEY')

            employee_info = self.client.update_employee(1, employee)
            self.assertIsInstance(employee_info, EmployeeInfo)
            self.assertEqual(employee_info.id, 1)
            self.assertEqual(employee_info.name, 'Ivanov Ivan Ivanovich')
            self.assertEqual(employee_info.login, 'test_login')
            self.assertEqual(employee_info.password, 'test_password')
            self.assertEqual(employee_info.pos_id, 'POS_KEY')

    def test_delete_order_success(self):
        with patch('komtet_kassa_sdk.client.requests') as requests:
            requests.delete.return_value = ResponseMock()

            result = self.client.delete_employee(1)
            self.assertEqual(result, True)


class TestHelpers(TestCase):
    def test_correction_positions(self):
        '''
        Тест корректировки позиций
        '''
        result = correction_positions([
            {'price': Decimal('42.4'), 'quantity': 2, 'total': Decimal('84.5')},
            {'price': Decimal('10'), 'quantity': 1, 'total': Decimal('10')}
        ])
        self.assertListEqual(result, [
            {'price': Decimal('42.10'), 'quantity': 1, 'total': Decimal('42.10')},
            {'price': Decimal('42.4'), 'quantity': 1, 'total': Decimal('42.40')},
            {'price': Decimal('10'), 'quantity': 1, 'total': Decimal('10')}
        ])
