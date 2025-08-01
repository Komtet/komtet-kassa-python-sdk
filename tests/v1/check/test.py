# -*- coding: utf-8 -*-
from decimal import Decimal
from unittest import TestCase

from komtet_kassa_sdk.v1 import (Agent, AgentType, CalculationMethod, CalculationSubject, Check,
                                 Intent, Nomenclature, TaxSystem)


class TestCheck(TestCase):
    def test_check(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON, payment_address='ул.Мира')
        check.add_payment(100)
        check.add_position('name 0', price=100, oid=1)
        check.add_payment(200)
        check.add_position('name 1', 100, quantity=2, measure_name='kg', oid='2')
        check.add_payment(300)
        check.add_position('name 2', 100, 3, total=290, vat=20)
        check.set_internet(True)
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
            'internet': True,
            'callback_url': 'http://test.pro'
        }
        for key, value in check:
            self.assertEqual(expected[key], value)

        check.set_print(True)
        self.assertTrue(check['print'])
        check.set_print(False)
        self.assertFalse(check['print'])

        check.set_internet(True)
        self.assertTrue(check['internet'])
        check.set_internet(False)
        self.assertFalse(check['internet'])

    def test_check_ffd_105_with_client_name(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_client(name='Иванов И.П.')

        self.assertEqual(check._data['client']['name'], 'Иванов И.П.')

    def test_check_ffd_105_with_client_inn(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_client(inn='1231231231')

        self.assertEqual(check._data['client']['inn'], '1231231231')

    def test_check_ffd_105_with_empty_client(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.set_client()

        self.assertEqual(check._data.get('client'), None)

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

    def test_position_user_data(self):
        '''
        Тест добавления дополнительного предмета расчёта
        '''

        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.add_position(oid=1, name='Позиция 1', price=Decimal('4'),
                           quantity=2, total=Decimal(8), user_data='предмет расёта')

        self.assertEqual(check['positions'][0]['user_data'], 'предмет расёта')

    def test_add_casheir(self):
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
        check.add_cashier('Pupkin', '7867234764782')

        expected = {
            'external_id': 1,
            'user': 'user@host',
            'print': False,
            'intent': 'sell',
            'sno': 0,
            'cashier': {
                'name': 'Pupkin',
                'inn': '7867234764782'
            },
            'payments': [],
            'positions': []
        }

        for key, value in check:
            self.assertEqual(expected[key], value)

    def test_add_cashless_payments(self):
        '''
        Тест добавления сведений об оплате в безналичном порядке
        '''
        check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)

        check.add_cashless_payment(sum=1000, method=1, id='transaction_1')
        self.assertEqual(len(check['cashless_payments']), 1)
        self.assertEqual(check['cashless_payments'][0], {
            'sum': 1000,
            'method': 1,
            'id': 'transaction_1'
        })

        check.add_cashless_payment(sum=2000, method=2, id='transaction_2',
                                additional_info='Дополнительные сведения')
        self.assertEqual(len(check['cashless_payments']), 2)
        self.assertEqual(check['cashless_payments'][1], {
            'sum': 2000,
            'method': 2,
            'id': 'transaction_2',
            'additional_info': 'Дополнительные сведения'
        })

        check.add_cashless_payment(sum=3000, method=3, id='transaction_3')
        self.assertEqual(len(check['cashless_payments']), 3)
        self.assertEqual(check['cashless_payments'][2], {
            'sum': 3000,
            'method': 3,
            'id': 'transaction_3'
        })


class TestNomenklature(TestCase):

    def test_nomenklature(self):
        nomenclature = Nomenclature('019876543210123421sgEKKPPcS25y5',
                                    '444D00000096b43f303132333432317367454b4b5050635332357935')

        self.assertEqual(nomenclature.code,
                         '019876543210123421sgEKKPPcS25y5')
        self.assertEqual(nomenclature['nomenclature_code']['code'],
                         '019876543210123421sgEKKPPcS25y5')
        self.assertEqual(nomenclature.hex_code,
                         '444D00000096b43f303132333432317367454b4b5050635332357935')
