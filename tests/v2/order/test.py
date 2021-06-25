# -*- coding: utf-8 -*-
from decimal import Decimal
from unittest import TestCase

from komtet_kassa_sdk.v2 import (Agent, AgentType, Client, Order, OrderInfo, PaymentType, VatRate)
from komtet_kassa_sdk.v2.client import Response
from mock import patch
from ...helpers.mock import (ResponseMock)


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
            "payment_type": PaymentType.CARD,
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
            "payment_type": PaymentType.CARD,
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
                         coordinate={'latitude': '53.202838856701206',
                                     'longitude': '44.99768890421866'})

        self.assertEqual(
            order._Order__data['client_coordinate']['latitude'], '53.202838856701206')
        self.assertEqual(
            order._Order__data['client_coordinate']['longitude'], '44.99768890421866')


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
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
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
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
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
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
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
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
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
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
            requests.post.return_value = self.response_mock

            order = Order(order_id=2589, is_paid=True, state='new', sno=0,
                          prepayment=200.0, payment_type=PaymentType.CASH)

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
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
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
