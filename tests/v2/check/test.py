# -*- coding: utf-8 -*-
from decimal import Decimal
from unittest import TestCase

from komtet_kassa_sdk.v2 import (Agent, AgentType, Check, Position, Intent, MarkTypes, MeasureTypes,
                                 PaymentMethod, PaymentObject, TaxSystem, VatRate)


class TestCheck(TestCase):
    def test_full_check(self):
        check = Check(oid=2043, intent=Intent.SELL)
        check.set_client(email='client@client.ru', phone='+79992410085',
                         name='Иванов Иван', inn='516974792202')
        check.set_company(payment_address='ул. им Дедушки на деревне д.5',
                          tax_system=TaxSystem.COMMON)

        agent_info = Agent(agent_type=AgentType.AGENT, phone='+79998887766',
                           name='Названиепоставщика', inn='287381373424')
        agent_info.set_paying_agent(operation='Операция1', phones=['+79998887766'])
        agent_info.set_receive_payments_operator(phones=['+79998887766'])
        agent_info.set_money_transfer_operator(phones=['+79998887766'], name='Операторперевода',
                                               address='г. Москва, ул. Складочная д.3',
                                               inn='8634330204')

        position = Position(id=1, name='Товар', price=10, quantity=1, total=10, excise=10,
                            measure=MeasureTypes.PIECE, declaration_number='12332234533',
                            user_data='Дополнительный реквизит предмета расчета',
                            country_code='056', payment_method=PaymentMethod.FULL_PAYMENT,
                            payment_object=PaymentObject.PRODUCT, vat=VatRate.RATE_NO)
        position.set_mark_code(type=MarkTypes.EAN13, code='1234567890123')
        position.set_mark_quantity(numerator=1, denominator=2)
        position.set_agent(agent_info)

        check.add_position(position)
        check.set_cashier(name='Кассир', inn='8634330201')
        check.set_additional_check_props('445334544')
        check.add_payment(10)
        check.set_callback_url('http://test.pro')

        expected = {
            'external_id': 2043,
            'intent': 'sell',
            'print': False,
            'client': {
                'email': 'client@client.ru',
                'phone': '+79992410085',
                'name': 'Иванов Иван',
                'inn': '516974792202'
            },
            'company': {
                'payment_address': 'ул. им Дедушки на деревне д.5',
                'sno': 0
            },
            'positions': [{
                'id': 1,
                'name': 'Товар',
                'price': 10,
                'quantity': 1,
                'total': 10,
                'measure': 0,
                'user_data': 'Дополнительный реквизит предмета расчета',
                'excise': 10,
                'country_code': '056',
                'declaration_number': '12332234533',
                'payment_method': 'full_payment',
                'payment_object': 'product',
                'mark_code': {
                    'ean13': '1234567890123'
                },
                'mark_quantity': {
                    'numerator': 1,
                    'denominator': 2
                },
                'vat': 'no',
                'agent_info': {
                    'type': 'agent',
                    'paying_agent': {
                        'operation': 'Операция1',
                        'phones': ['+79998887766']
                    },
                    'receive_payments_operator': {
                        'phones': ['+79998887766']
                    },
                    'money_transfer_operator': {
                        'phones': ['+79998887766'],
                        'name': 'Операторперевода',
                        'address': 'г. Москва, ул. Складочная д.3',
                        'inn': '8634330204'
                    }
                },
                'supplier_info': {
                    'phones': ['+79998887766'],
                    'name': 'Названиепоставщика',
                    'inn': '287381373424'
                }
            }],
            'cashier': {
                'name': 'Кассир',
                'inn': '8634330201'
            },
            'additional_check_props': '445334544',
            'payments': [{
                'type': 'card',
                'sum': 10
            }],
            'callback_url': 'http://test.pro'
        }

        for key, value in check:
            self.assertEqual(expected[key], value)

        check.set_print(True)
        self.assertTrue(check['print'])
        check.set_print(False)
        self.assertFalse(check['print'])

    def test_minimal_check(self):
        check = Check(oid=2, intent=Intent.SELL)
        check.set_client(email='client@client.ru')
        check.set_company(payment_address='ул. им Дедушки на деревне д.5',
                          tax_system=TaxSystem.COMMON)

        position = Position(id=1, name='Товар', price=10, quantity=1,
                            measure=MeasureTypes.PIECE, payment_method=PaymentMethod.FULL_PAYMENT,
                            payment_object=PaymentObject.PRODUCT, vat=VatRate.RATE_NO)
        check.add_position(position)
        check.set_cashier(name='Кассир')
        check.add_payment(10)

        expected = {
            'external_id': 2,
            'intent': 'sell',
            'print': False,
            'client': {
                'email': 'client@client.ru'
            },
            'company': {
                'payment_address': 'ул. им Дедушки на деревне д.5',
                'sno': 0
            },
            'positions': [{
                'id': 1,
                'name': 'Товар',
                'price': 10,
                'quantity': 1,
                'total': 10,
                'measure': 0,
                'payment_method': 'full_payment',
                'payment_object': 'product',
                'vat': 'no',
            }],
            'cashier': {
                'name': 'Кассир',
            },
            'payments': [{
                'type': 'card',
                'sum': 10
            }]
        }

        for key, value in check:
            self.assertEqual(expected[key], value)

        check.set_print(True)
        self.assertTrue(check['print'])
        check.set_print(False)
        self.assertFalse(check['print'])

    def test_company_in_check(self):
        check = Check(oid=2, intent=Intent.SELL)
        check.set_company(payment_address='ул. им Дедушки на деревне д.5', inn='123456789',
                          tax_system=TaxSystem.COMMON, place_address='Ещё один аддрес')

        expected = {
            'external_id': 2,
            'intent': 'sell',
            'print': False,
            'company': {
                'payment_address': 'ул. им Дедушки на деревне д.5',
                'sno': 0,
                'inn': '123456789',
                'place_address': 'Ещё один аддрес'
            },
            'client': {},
            'payments': [],
            'positions': []
        }

        for key, value in check:
            self.assertEqual(expected[key], value)

    def test_client_in_check(self):
        check = Check(oid=2, intent=Intent.SELL)
        check.set_client(email='client@client.ru', phone='+70002410085',
                         name='Иванов Иван Иванович', inn='516974792202', birthdate='18.11.1990',
                         citizenship='643', document_code='21', document_data='4507 443564',
                         address='г.Москва, Ленинский проспект д.1 кв 43')

        expected = {
            'external_id': 2,
            'intent': 'sell',
            'print': False,
            'company': {},
            'client': {
                'email': 'client@client.ru',
                'phone': '+70002410085',
                'name': 'Иванов Иван Иванович',
                'inn': '516974792202',
                'birthdate': '18.11.1990',
                'citizenship': '643',
                'document_code': '21',
                'document_data': '4507 443564',
                'address': 'г.Москва, Ленинский проспект д.1 кв 43'
            },
            'payments': [],
            'positions': []
        }

        for key, value in check:
            self.assertEqual(expected[key], value)

    def test_apply_discount(self):
        check = Check(oid=2043, intent=Intent.SELL)
        position = Position(id=1, name='Товар1', price=120.67, quantity=1,
                            measure=MeasureTypes.PIECE, vat=VatRate.RATE_NO,
                            payment_method=PaymentMethod.FULL_PAYMENT,
                            payment_object=PaymentObject.PRODUCT)
        check.add_position(position)
        position = Position(id=2, name='Товар2', price=113.54, quantity=1,
                            measure=MeasureTypes.PIECE, vat=VatRate.RATE_NO,
                            payment_method=PaymentMethod.FULL_PAYMENT,
                            payment_object=PaymentObject.PRODUCT)
        check.add_position(position)
        check.apply_discount(50)

        self.assertEqual(check['positions'][0]['total'], Decimal('94.91'))
        self.assertEqual(check['positions'][1]['total'], Decimal('89.30'))

    def test_apply_correction_positions(self):
        '''
        Тест применения алгоритма корректировки позиции
        '''
        check = Check(oid=2043, intent=Intent.SELL)
        position = Position(id=1, name='Товар', price=Decimal('42.4'), quantity=2,
                            total=Decimal(84.5), measure=MeasureTypes.PIECE, vat=VatRate.RATE_NO,
                            payment_method=PaymentMethod.FULL_PAYMENT,
                            payment_object=PaymentObject.PRODUCT)
        check.add_position(position)
        check.apply_correction_positions()

        self.assertEqual(len(check['positions']), 2)

    def test_marked_position(self):
        '''
        Тест маркированной позиции
        '''
        check = Check(oid=2043, intent=Intent.SELL)
        position = Position(id=1, name='Товар', price=10, quantity=1,
                            measure=MeasureTypes.PIECE, vat=VatRate.RATE_NO,
                            payment_method=PaymentMethod.FULL_PAYMENT,
                            payment_object=PaymentObject.PRODUCT)
        position.set_mark_code(type=MarkTypes.EAN13, code='1234567890123')
        position.set_mark_quantity(numerator=1, denominator=2)
        check.add_position(position)

        self.assertEqual(check['positions'][0]['mark_code']['ean13'], '1234567890123')
        self.assertEqual(check['positions'][0]['mark_quantity']['numerator'], 1)
        self.assertEqual(check['positions'][0]['mark_quantity']['denominator'], 2)

    def test_additional_user_props(self):
        '''
        Тест дополнительных параметров чека
        '''
        check = Check(oid=2043, intent=Intent.SELL)
        check.set_additional_user_props('получатель', 'Васильев')

        self.assertEqual(check['additional_user_props']['name'], 'получатель')
        self.assertEqual(check['additional_user_props']['value'], 'Васильев')

    def test_sectoral_check_props(self):
        '''
        Тест данных об отраслевой принадлежности чека
        '''
        check = Check(oid=2043, intent=Intent.SELL)
        check.add_sectoral_check_props('001', '01.01.2001', '170/21',
                                       'Ид1=Знач1&Ид2=Знач2&Ид3=Знач3')

        self.assertEqual(check['sectoral_check_props'][0]['federal_id'], '001')
        self.assertEqual(check['sectoral_check_props'][0]['date'], '01.01.2001')
        self.assertEqual(check['sectoral_check_props'][0]['number'], '170/21')
        self.assertEqual(check['sectoral_check_props'][0]['value'], 'Ид1=Знач1&Ид2=Знач2&Ид3=Знач3')

    def test_wholesale(self):
        ''' Тест установки признака использования ОСУ
        '''
        position = Position(
            id=1,
            name='Товар1',
            price=120.67,
            quantity=1,
            measure=MeasureTypes.PIECE,
            vat=VatRate.RATE_NO,
            payment_method=PaymentMethod.FULL_PAYMENT,
            payment_object=PaymentObject.PRODUCT
        )
        position.set_wholesale(True)
        self.assertTrue(position['wholesale'])
        position.set_wholesale(False)
        self.assertFalse(position['wholesale'])

    def test_sectoral_item_props(self):
        '''
        Тест данных об отраслевой принадлежности чека
        '''
        check = Check(oid=2043, intent=Intent.SELL)
        position = Position(id=1, name='Товар1', price=120.67, quantity=1,
                            measure=MeasureTypes.PIECE, vat=VatRate.RATE_NO,
                            payment_method=PaymentMethod.FULL_PAYMENT,
                            payment_object=PaymentObject.PRODUCT)
        position.add_sectoral_item_props('001', '01.01.2001', '170/21',
                                         'Ид1=Знач1&Ид2=Знач2&Ид3=Знач3')
        check.add_position(position)

        self.assertEqual(check['positions'][0]['sectoral_item_props'][0]['federal_id'], '001')
        self.assertEqual(check['positions'][0]['sectoral_item_props'][0]['date'], '01.01.2001')
        self.assertEqual(check['positions'][0]['sectoral_item_props'][0]['number'], '170/21')
        self.assertEqual(check['positions'][0]['sectoral_item_props'][0]['value'],
                         'Ид1=Знач1&Ид2=Знач2&Ид3=Знач3')

    def test_operating_check_props(self):
        '''
        Тест данных об отраслевой принадлежности чека
        '''
        check = Check(oid=2043, intent=Intent.SELL)
        check.set_operating_check_props('0', 'Данные операции', '03.11.2020 12:05:31')

        self.assertEqual(check['operating_check_props']['name'], '0')
        self.assertEqual(check['operating_check_props']['value'], 'Данные операции')
        self.assertEqual(check['operating_check_props']['timestamp'], '03.11.2020 12:05:31')


class TestCheckAgent(TestCase):

    def test_agent(self):
        check = Check(oid=2043, intent=Intent.SELL)

        agent_info = Agent(agent_type=AgentType.AGENT, phone='+79998887766',
                           name='Названиепоставщика', inn='287381373424')
        agent_info.set_paying_agent(operation='Операция1', phones=['+79998887766'])
        agent_info.set_receive_payments_operator(phones=['+78005553535'])
        agent_info.set_money_transfer_operator(phones=['+79998887766'], name='Операторперевода',
                                               address='г. Москва, ул. Складочная д.3',
                                               inn='8634330204')
        position = Position(id=1, name='Товар1', price=100, quantity=1,
                            measure=MeasureTypes.PIECE, vat=VatRate.RATE_NO,
                            payment_method=PaymentMethod.FULL_PAYMENT,
                            payment_object=PaymentObject.PRODUCT)
        position.set_agent(agent_info)
        check.add_position(position)

        position = dict(check)['positions'][0]
        self.assertIn('agent_info', position)
        self.assertEqual(position['agent_info']['type'], 'agent')

        self.assertIn('paying_agent', position['agent_info'])
        self.assertDictEqual(position['agent_info']['paying_agent'],
                             {'operation': 'Операция1', 'phones': ['+79998887766']})

        self.assertIn('receive_payments_operator', position['agent_info'])
        self.assertDictEqual(position['agent_info']['receive_payments_operator'], {
                             "phones": ["+78005553535"]})

        self.assertIn('money_transfer_operator', position['agent_info'])
        self.assertDictEqual(position['agent_info']['money_transfer_operator'],
                             {'phones': ['+79998887766'], 'name': 'Операторперевода',
                              'address': 'г. Москва, ул. Складочная д.3', 'inn': '8634330204'})

        self.assertIn('supplier_info', position)
        self.assertDictEqual(position['supplier_info'],
                             {'phones': ['+79998887766'], 'name': 'Названиепоставщика',
                              'inn': '287381373424'})


class TestSetCashier(TestCase):

    def test_set_cashier_with_inn_in_check(self):
        check = Check(oid=1, intent=Intent.SELL)
        check.set_cashier('Иваров И.П.', '1234567890123')
        self.assertDictEqual(check['cashier'], {
            'name': 'Иваров И.П.',
            'inn': '1234567890123'
        })

    def test_set_cashier_without_inn_in_check(self):
        check = Check(oid=1, intent=Intent.SELL)
        check.set_cashier('Иваров И.П.')
        self.assertDictEqual(check['cashier'], {
            'name': 'Иваров И.П.'
        })
