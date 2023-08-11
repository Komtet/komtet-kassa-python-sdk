# -*- coding: utf-8 -*-
from decimal import Decimal
from unittest import TestCase

from komtet_kassa_sdk.v2 import (Agent, AgentType, Client, MarkTypes, Order, OrderInfo, OrderItem,
                                 PaymentType, TaxSystem, VatRate)
from komtet_kassa_sdk.v2.client import Response
from mock import patch

from ...helpers.mock import ResponseMock


class TestOrder(TestCase):
    def test_order(self):
        self.maxDiff = None
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        order.set_client(email='client@client.ru', phone='+79992410085', name='Иванов Иван',
                         address='ул. Кижеватова д.7 кв.30',
                         coordinate={'latitude': '53.202838856701206',
                                     'longitude': '44.99768890421866'},
                         requisites={'name': 'Иванов Иван', 'inn': '516974792202'})
        order.set_delivery_time('01.01.2021 12:00', '01.01.2021 13:00')
        order.set_description('Комментарий к заказу')
        order.add_item(OrderItem(id=1, name='Пицца маргарита', price=500, quantity=1,
                                 measure=0, total=500, type='product'))
        order.add_item(OrderItem(id=2, name='Пицца пеперони', price=600, quantity=5,
                                 measure=0, total=3000, type='product', vat=VatRate.RATE_10))
        order.add_item(OrderItem(id=3, name='Пицца барбекю', price=555, quantity=1,
                                 measure=0, type='product_practical', excise=19.89, country_code='643',
                                 declaration_number='10129000/220817/0211234'))

        expected = {
            'client': {
                'address': 'ул. Кижеватова д.7 кв.30',
                'coordinate': {
                    'latitude': '53.202838856701206',
                    'longitude': '44.99768890421866'
                },
                'email': 'client@client.ru',
                'name': 'Иванов Иван',
                'phone': '+79992410085',
                'requisites': {
                    'inn': '516974792202',
                    'name': 'Иванов Иван',
                }
            },
            'date_end': '01.01.2021 13:00',
            'date_start': '01.01.2021 12:00',
            'description': 'Комментарий к заказу',
            'external_id': 12,
            'is_pay_to_courier': True,
            'items': [
                {
                    'id': 1,
                    'is_need_nomenclature_code': False,
                    'measure': 0,
                    'name': 'Пицца маргарита',
                    'price': 500,
                    'quantity': 1,
                    'total': 500,
                    'type': 'product',
                    'vat': 'no'
                },
                {
                    'id': 2,
                    'is_need_nomenclature_code': False,
                    'measure': 0,
                    'name': 'Пицца пеперони',
                    'price': 600,
                    'quantity': 5,
                    'total': 3000,
                    'type': 'product',
                    'vat': '10'
                },
                {
                    'country_code': '643',
                    'declaration_number': '10129000/220817/0211234',
                    'excise': 19.89,
                    'id': 3,
                    'is_need_nomenclature_code': False,
                    'measure': 0,
                    'name': 'Пицца барбекю',
                    'price': 555,
                    'quantity': 1,
                    'total': 555,
                    'type': 'product_practical',
                    'vat': 'no'
                }
            ],
            'payment_type': 'card',
            'prepayment': 200,
            'state': 'new'
        }

        for key, value in order:
            self.assertEqual(expected[key], value)

    def test_order_with_callback_url(self):
        self.maxDiff = None
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        order.set_client(email='client@client.ru', phone='+79992410085', name='Иванов Иван',
                         address='ул. Кижеватова д.7 кв.30',
                         coordinate={'latitude': '53.202838856701206',
                                     'longitude': '44.99768890421866'},
                         requisites={'name': 'Иванов Иван', 'inn': '516974792202'})
        order.set_delivery_time('01.01.2021 12:00', '01.01.2021 13:00')
        order.set_description('Комментарий к заказу')
        order.add_item(OrderItem(id=1, name='Пицца маргарита', price=500, quantity=1, product_id=15,
                                 measure=0, total=500, type='product_practical', external_id=10,
                                 user_data='Дополнительный реквизит предмета расчета'))

        order.add_callback_url('https://callback_url.ru')
        order.set_courier_id(1)

        expected = {
            'callback_url': 'https://callback_url.ru',
            'client': {
                'address': 'ул. Кижеватова д.7 кв.30',
                'coordinate': {
                    'latitude': '53.202838856701206',
                    'longitude': '44.99768890421866'
                },
                'email': 'client@client.ru',
                'name': 'Иванов Иван',
                'phone': '+79992410085',
                'requisites': {
                    'inn': '516974792202',
                    'name': 'Иванов Иван',
                }
            },
            'courier_id': 1,
            'date_end': '01.01.2021 13:00',
            'date_start': '01.01.2021 12:00',
            'description': 'Комментарий к заказу',
            'external_id': 12,
            'is_pay_to_courier': True,
            'items': [
                {
                    'id': 1,
                    'external_id': 10,
                    'is_need_nomenclature_code': False,
                    'measure': 0,
                    'name': 'Пицца маргарита',
                    'price': 500,
                    'quantity': 1,
                    'total': 500,
                    'type': 'product_practical',
                    'vat': 'no',
                    'product_id': 15,
                    'user_data': 'Дополнительный реквизит предмета расчета'
                }
            ],
            'payment_type': 'card',
            'prepayment': 200,
            'state': 'new'
        }

        for key, value in order:
            self.assertEqual(expected[key], value)

    def test_order_with_full_company(self):
        self.maxDiff = None
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        order.set_company(payment_address='ул. им Дедушки на деревне д.5', inn='123456789',
                          tax_system=TaxSystem.COMMON, place_address='Ещё один аддрес',
                          email='company@gmail.com')

        expected = {
            'company': {
                'email': 'company@gmail.com',
                'inn': '123456789',
                'payment_address': 'ул. им Дедушки на деревне д.5',
                'place_address': 'Ещё один аддрес',
                'sno': 0
            },
            'description': '',
            'external_id': 12,
            'is_pay_to_courier': True,
            'items': [],
            'payment_type': 'card',
            'prepayment': 200,
            'state': 'new'
        }

        for key, value in order:
            self.assertEqual(expected[key], value)

    def test_order_with_courier(self):
        self.maxDiff = None
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        order.set_courier_id(1)

        expected = {
            'courier_id': 1,
            'description': '',
            'external_id': 12,
            'is_pay_to_courier': True,
            'items': [],
            'payment_type': 'card',
            'prepayment': 200,
            'state': 'new'
        }

        for key, value in order:
            self.assertEqual(expected[key], value)

    def test_order_with_additional_user_props(self):
        self.maxDiff = None
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        order.set_additional_user_props('получатель', 'Васильев')

        expected = {
            'additional_user_props': {
                'name': 'получатель',
                'value': 'Васильев'
            },
            'description': '',
            'external_id': 12,
            'is_pay_to_courier': True,
            'items': [],
            'payment_type': 'card',
            'prepayment': 200,
            'state': 'new'
        }

        for key, value in order:
            self.assertEqual(expected[key], value)

    def test_order_with_additional_check_props(self):
        self.maxDiff = None
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        order.set_additional_check_props('445334544')

        expected = {
            'additional_check_props': '445334544',
            'description': '',
            'external_id': 12,
            'is_pay_to_courier': True,
            'items': [],
            'payment_type': 'card',
            'prepayment': 200,
            'state': 'new'
        }

        for key, value in order:
            self.assertEqual(expected[key], value)

    def test_order_with_sectorals_props(self):
        self.maxDiff = None
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        order.add_sectoral_check_props('001', '01.01.2001', '170/21',
                                       'Ид1=Знач1&Ид2=Знач2&Ид3=Знач3')
        item = OrderItem(id=1, name='Некий продукт', price=120.67, quantity=1,
                         measure=0, type='product', is_need_nomenclature_code=True)
        item.add_sectoral_item_props('001', '01.01.2001', '170/21',
                                     'Ид1=Знач1&Ид2=Знач2&Ид3=Знач3')
        order.add_item(item)

        expected = {
            'description': '',
            'external_id': 12,
            'is_pay_to_courier': True,
            'items': [{
                      'id': 1,
                      'is_need_nomenclature_code': True,
                      'measure': 0,
                      'name': 'Некий продукт',
                      'price': 120.67,
                      'quantity': 1,
                      'sectoral_item_props': [{
                          'date': '01.01.2001',
                          'federal_id': '001',
                          'number': '170/21',
                          'value': 'Ид1=Знач1&Ид2=Знач2&Ид3=Знач3'
                      }],
                      'total': 120.67,
                      'type': 'product',
                      'vat': 'no'
                      }],
            'payment_type': 'card',
            'prepayment': 200,
            'sectoral_check_props': [{
                'date': '01.01.2001',
                'federal_id': '001',
                'number': '170/21',
                'value': 'Ид1=Знач1&Ид2=Знач2&Ид3=Знач3'
            }],
            'state': 'new'
        }

        for key, value in order:
            self.assertEqual(expected[key], value)

    def test_order_with_operating_check_props(self):
        self.maxDiff = None
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        order.set_operating_check_props('0', 'Данные операции', '03.11.2020 12:05:31')

        expected = {
            'description': '',
            'external_id': 12,
            'is_pay_to_courier': True,
            'items': [],
            'operating_check_props': {
                'name': '0',
                'timestamp': '03.11.2020 12:05:31',
                'value': 'Данные операции'
            },
            'payment_type': 'card',
            'prepayment': 200,
            'state': 'new'
        }

        for key, value in order:
            self.assertEqual(expected[key], value)

    def test_apply_discount(self):
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        order.add_item(OrderItem(id=1, name='Пицца маргарита', price=120.67, quantity=1,
                                 measure=0, type='product'))
        order.add_item(OrderItem(id=2, name='Пицца пеперони', price=113.54, quantity=1,
                                 measure=0, type='product', ))
        order.apply_discount(50)

        self.assertEqual(order['items'][0]['total'], Decimal('94.91'))
        self.assertEqual(order['items'][1]['total'], Decimal('89.30'))

    def test_position_add_mark_code(self):
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        item = OrderItem(id=1, name='Некий продукт', price=120.67, quantity=1,
                         measure=0, type='product', is_need_nomenclature_code=False)
        item.set_mark_code(MarkTypes.GS1M, '019876543210123421sgEKKPPcS25y5')
        order.add_item(item)

        self.assertEqual(order['items'][0]['mark_code']['gs1m'], '019876543210123421sgEKKPPcS25y5')
        self.assertFalse(order['items'][0]['is_need_nomenclature_code'])

    def test_position_add_mark_quantity(self):
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        item = OrderItem(id=1, name='Некий продукт', price=120.67, quantity=1,
                         measure=0, type='product', is_need_nomenclature_code=True)
        item.set_mark_quantity(10, 1)
        order.add_item(item)

        self.assertEqual(order['items'][0]['mark_quantity']['numerator'], 10)
        self.assertEqual(order['items'][0]['mark_quantity']['denominator'], 1)
        self.assertTrue(order['items'][0]['is_need_nomenclature_code'])

    def test_add_client_longitude_latitude(self):
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        order.set_client(email='client@client.ru', phone='+79992410085', name='Иванов Иван',
                         address='ул. Кижеватова д.7 кв.30',
                         coordinate={'latitude': '53.202838856701206',
                                     'longitude': '44.99768890421866'},
                         requisites={'name': 'Иванов Иван', 'inn': '516974792202'})

        self.assertEqual(
            order._Order__data['client']['coordinate']['latitude'], '53.202838856701206')
        self.assertEqual(
            order._Order__data['client']['coordinate']['longitude'], '44.99768890421866')


class TestClientOrder(TestCase):
    def setUp(self):
        self.client = Client('shop-id', 'secret-key')
        json = {
            'id': 775,
            'client': {
                'address': 'обл Пензенская, Пенза',
                'name': 'test test test',
                'phone': '88005553535'
            },
            'company': {
                'payment_address': 'ул. Кижеватова д.7 кв.30',
                'sno': 0
            },
            'date_end': '2019-04-12 13:00',
            'date_start': '2019-04-12 07:00',
            'description': '',
            'external_id': 12,
            'is_pay_to_courier': False,
            'items': [{
                'id': 1,
                'is_need_nomenclature_code': False,
                'measure': 0,
                'name': 'Демо-товар 2',
                'price': 1500.0,
                'quantity': 5.0,
                'total': 7500.0,
                'type': 'product',
                'vat': '10'
            },
                {
                    'id': 2,
                'is_need_nomenclature_code': False,
                'measure': 0,
                'name': 'Доставка',
                'price': 500.0,
                'quantity': 1.0,
                'total': 500.0,
                'type': 'service',
                'vat': 'no'
            }],
            'amount': 8000.0,
            'payment_type': 'cash',
            'prepayment': 200.0,
            'state': 'new',
            'callback_url': 'https://calback_url.ru'
        }
        self.response_mock = ResponseMock(**json)

    def test_create_order_success(self):
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
            requests.post.return_value = self.response_mock

            order = Order(12, state='new', is_pay_to_courier=False, payment_type=PaymentType.CARD)
            order.set_company(payment_address='ул. Кижеватова д.7 кв.30', tax_system=0)
            order.set_client(name='test test test',
                             address='обл Пензенская, Пенза',
                             phone='88005553535')
            order.set_delivery_time(date_start='2019-04-12 07:00', date_end='2019-04-12 13:00')
            order.add_item(OrderItem(id=1, name='Демо-товар 2', price=1500, quantity=5,
                                     measure=0, total=7500, vat='10', type='product'))
            order.add_item(OrderItem(id=2, name='Доставка', price=500, type='service'))

            order_info = self.client.create_order(order)

            self.assertIsInstance(order_info, OrderInfo)
            self.assertEqual(order_info.id, 775)
            self.assertEqual(order_info.state, 'new')
            self.assertDictEqual(order_info.items[0], {
                'id': 1,
                'is_need_nomenclature_code': False,
                'measure': 0,
                'name': 'Демо-товар 2',
                'price': 1500.0,
                'quantity': 5.0,
                'total': 7500.0,
                'type': 'product',
                'vat': '10'
            })
            self.assertDictEqual(order_info.items[1], {
                'id': 2,
                'is_need_nomenclature_code': False,
                'measure': 0,
                'name': 'Доставка',
                'price': 500.0,
                'quantity': 1.0,
                'total': 500.0,
                'type': 'service',
                'vat': 'no'
            })

    def test_update_order_success(self):
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
            requests.put.return_value = self.response_mock

            order = Order(external_id=12, state='new', is_pay_to_courier=False,
                          payment_type=PaymentType.CARD)
            order.set_client(email='client@client.ru', phone='+79992410085', name='Иванов Иван',
                             address='ул. Кижеватова д.7 кв.30',
                             coordinate={'latitude': '53.202838856701206',
                                         'longitude': '44.99768890421866'},
                             requisites={'name': 'Иванов Иван', 'inn': '516974792202'})
            order.set_company(payment_address='ул. Кижеватова д.7 кв.30', tax_system=0)
            order.set_delivery_time(date_start='2019-04-12 07:00', date_end='2019-04-12 13:00')
            order.add_item(OrderItem(id=1, name='Демо-товар 2', price=1500, quantity=5,
                                     measure=0, total=7500, vat='10', type='product'))
            order.add_item(OrderItem(id=2, name='Доставка', price=500, type='service'))

            order_info = self.client.update_order(775, order)
            self.assertIsInstance(order_info, OrderInfo)
            self.assertEqual(order_info.id, 775)
            self.assertEqual(order_info.state, 'new')
            self.assertEqual(order_info.amount, 8000.0)

    def test_get_order_info_success(self):
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
            requests.get.return_value = self.response_mock
            order_info = self.client.get_order_info(775)
            self.assertIsInstance(order_info, OrderInfo)
            self.assertEqual(order_info.id, 775)
            self.assertEqual(order_info.client['name'], 'test test test')
            self.assertEqual(order_info.state, 'new')
            self.assertEqual(order_info.client['phone'], '88005553535')

            self.assertDictEqual(order_info.items[0], {
                'id': 1,
                'is_need_nomenclature_code': False,
                'measure': 0,
                'name': 'Демо-товар 2',
                'price': 1500.0,
                'quantity': 5.0,
                'total': 7500.0,
                'type': 'product',
                'vat': '10'
            })
            self.assertDictEqual(order_info.items[1], {
                'id': 2,
                'is_need_nomenclature_code': False,
                'measure': 0,
                'name': 'Доставка',
                'price': 500.0,
                'quantity': 1.0,
                'total': 500.0,
                'type': 'service',
                'vat': 'no'
            })

    def test_create_order_with_callback_url_success(self):
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
            requests.post.return_value = self.response_mock

            order = Order(12, state='new', is_pay_to_courier=False, payment_type=PaymentType.CARD)
            order.set_company(payment_address='ул. Кижеватова д.7 кв.30', tax_system=0)
            order.set_client(name='test test test',
                             address='обл Пензенская, Пенза',
                             phone='88005553535')
            order.set_delivery_time(date_start='2019-04-12 07:00', date_end='2019-04-12 13:00')
            order.add_item(OrderItem(id=1, name='Демо-товар 2', price=1500, quantity=5,
                                     measure=0, total=7500, vat='10', type='product'))
            order.add_item(OrderItem(id=2, name='Доставка', price=500, type='service'))
            order.add_callback_url('https://calback_url.ru')

            order_info = self.client.create_order(order)
            self.assertIsInstance(order_info, OrderInfo)
            self.assertEqual(order_info.id, 775)
            self.assertEqual(order_info.state, 'new')
            self.assertEqual(order_info.callback_url, 'https://calback_url.ru')

            self.assertDictEqual(order_info.items[0], {
                'id': 1,
                'is_need_nomenclature_code': False,
                'measure': 0,
                'name': 'Демо-товар 2',
                'price': 1500.0,
                'quantity': 5.0,
                'total': 7500.0,
                'type': 'product',
                'vat': '10'
            })
            self.assertDictEqual(order_info.items[1], {
                'id': 2,
                'is_need_nomenclature_code': False,
                'measure': 0,
                'name': 'Доставка',
                'price': 500.0,
                'quantity': 1.0,
                'total': 500.0,
                'type': 'service',
                'vat': 'no'
            })

    def test_set_payment_type_and_prepayment(self):
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
            requests.post.return_value = self.response_mock

            order = Order(external_id=12, state='new', is_pay_to_courier=False,
                          payment_type=PaymentType.CASH, prepayment=200.0)

            order_info = self.client.create_order(order)
            self.assertIsInstance(order_info, OrderInfo)

            self.assertEqual(order_info.payment_type, 'cash')
            self.assertEqual(order_info.prepayment, 200.0)

    def test_apply_correction_positions(self):
        '''
        Тест применения алгоритма корректировки позиции
        '''
        order = Order(12, state='new', is_pay_to_courier=False, payment_type=PaymentType.CARD)
        order.add_item(OrderItem(id=1, name='Позиция 1', price=Decimal('42.4'), quantity=2,
                                 measure=0, vat='10', total=Decimal(84.5), type='product'))
        order.add_item(OrderItem(id=2, name='Доставка', price=10, type='service'))

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

    def test_order_with_agent(self):
        self.maxDiff = None
        order = Order(12, state='new', is_pay_to_courier=True,
                      prepayment=200, payment_type=PaymentType.CARD)
        order.set_client(email='client@client.ru', phone='+79992410085', name='Иванов Иван',
                         address='ул. Кижеватова д.7 кв.30',
                         coordinate={'latitude': '53.202838856701206',
                                     'longitude': '44.99768890421866'},
                         requisites={'name': 'Иванов Иван', 'inn': '516974792202'})
        order.set_delivery_time('01.01.2021 12:00', '01.01.2021 13:00')
        order.set_description('Комментарий к заказу')
        item = OrderItem(id=1, name='Пицца маргарита', price=500, quantity=1,
                         measure=0, total=500, type='product')
        agent_info = Agent(agent_type=AgentType.AGENT, phone='+79998887766',
                           name='Названиепоставщика', inn='287381373424')
        agent_info.set_paying_agent(operation='Операция1', phones=['+79998887766'])
        agent_info.set_receive_payments_operator(phones=['+78005553535'])
        agent_info.set_money_transfer_operator(phones=['+79998887766'], name='Операторперевода',
                                               address='г. Москва, ул. Складочная д.3',
                                               inn='8634330204')
        item.set_agent(agent_info)
        order.add_item(item)

        expected = {
            'client': {
                'address': 'ул. Кижеватова д.7 кв.30',
                'coordinate': {
                    'latitude': '53.202838856701206',
                    'longitude': '44.99768890421866'
                },
                'email': 'client@client.ru',
                'name': 'Иванов Иван',
                'phone': '+79992410085',
                'requisites': {
                    'inn': '516974792202',
                    'name': 'Иванов Иван',
                }
            },
            'date_end': '01.01.2021 13:00',
            'date_start': '01.01.2021 12:00',
            'description': 'Комментарий к заказу',
            'external_id': 12,
            'is_pay_to_courier': True,
            'items': [{
                      'agent_info': {
                          'money_transfer_operator': {
                              'address': 'г. Москва, ул. Складочная д.3',
                              'inn': '8634330204',
                              'name': 'Операторперевода',
                              'phones': ['+79998887766']
                          },
                          'paying_agent': {
                              'operation': 'Операция1',
                              'phones': ['+79998887766']
                          },
                          'receive_payments_operator': {
                              'phones': ['+78005553535']
                          },
                          'type': 'agent'
                      },
                      'id': 1,
                      'is_need_nomenclature_code': False,
                      'measure': 0,
                      'name': 'Пицца маргарита',
                      'price': 500,
                      'quantity': 1,
                      'supplier_info': {
                          'inn': '287381373424',
                          'name': 'Названиепоставщика',
                          'phones': ['+79998887766']
                      },
                      'total': 500,
                      'type': 'product',
                      'vat': 'no'
                      }],
            'payment_type': 'card',
            'prepayment': 200,
            'state': 'new'
        }

        for key, value in order:
            self.assertEqual(expected[key], value)
