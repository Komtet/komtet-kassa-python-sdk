# -*- coding: utf-8 -*-
from decimal import Decimal
from unittest import TestCase

from komtet_kassa_sdk.v2 import (Agent, AgentType, Check, Position, Intent, MarkTypes, MesureTypes,
                                 PaymentMethod, PaymentObject, TaxSystem, VatRate)


class TestCheck(TestCase):
    def test_full_check(self):
        check = Check(oid=2043, intent=Intent.SELL)
        check.set_client(email='client@client.ru', phone='+79992410085',
                         name='Иванов Иван', inn='516974792202')
        check.set_company(payment_address='ул. им Дедушки на деревне д.5',
                          tax_system=TaxSystem.COMMON)

        agent_info = Agent(agent_type=AgentType.AGENT)
        agent_info.set_paying_agent(operation='Операция1', phones=['+79998887766'])
        agent_info.set_receive_payments_operator(phones=['+79998887766'])
        agent_info.set_money_transfer_operator(phones=['+79998887766'], name='Операторперевода',
                                               address='г. Москва, ул. Складочная д.3',
                                               inn='8634330204')

        position = Position(id=1, name='Товар', price=10, quantity=1, total=10, excise=10,
                            measure=MesureTypes.PIECE, declaration_number='12332234533',
                            user_data='Дополнительный реквизит предмета расчета',
                            country_code='056', payment_method=PaymentMethod.FULL_PAYMENT,
                            payment_object=PaymentObject.PRODUCT, vat=VatRate.RATE_NO)
        position.set_mark_code(type=MarkTypes.EAN13, code='1234567890123')
        position.set_mark_quantity(numerator=1, denominator=2)
        position.set_agent(agent_info)
        position.set_supplier(phones=['+79998887766'], name='Названиепоставщика',
                              inn='287381373424')

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
                'payment_object': 0,
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

    # def test_check_ffd_105_with_client_name(self):
    #     check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
    #     check.set_client(name='Иванов И.П.')

    #     self.assertEqual(check._Check__data['client']['name'], 'Иванов И.П.')

    # def test_check_ffd_105_with_client_inn(self):
    #     check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
    #     check.set_client(inn='1231231231')

    #     self.assertEqual(check._Check__data['client']['inn'], '1231231231')

    # def test_check_ffd_105_with_empty_client(self):
    #     check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
    #     check.set_client()

    #     self.assertEqual(check._Check__data.get('client'), None)

    # def test_check_ffd_105(self):
    #     check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
    #     check.set_client(name='Иванов И.П.', inn='1231231231')
    #     check.set_cashier('Иваров И.П.', '1234567890123')
    #     check.add_payment(100)

    #     agent = Agent(AgentType.COMMISSIONAIRE, "+77777777777", "ООО 'Лютик'", "12345678901")
    #     self.assertEqual(agent['supplier_info']['inn'], '12345678901')

    #     nomenclature = Nomenclature()
    #     nomenclature.code = '019876543210123421sgEKKPPcS25y5'
    #     check.add_position('name 0', price=100, oid=1,
    #                        calculation_method=CalculationMethod.FULL_PAYMENT,
    #                        calculation_subject=CalculationSubject.PRODUCT,
    #                        agent=agent, nomenclature=nomenclature, excise=19.89,
    #                        country_code='643', declaration_number='10129000/220817/0211234')

    #     nomenclature = Nomenclature()
    #     nomenclature.code = '019876543210123421sgEKKPPcS25y5'
    #     nomenclature.hex_code = '444D00000096b43f303132333432317367454b4b5050635332357935'
    #     check.add_position('name 1', 100, quantity=2, measure_name='kg', oid='2',
    #                        nomenclature=nomenclature)

    #     nomenclature = Nomenclature()
    #     nomenclature.hex_code = '444D00000096b43f303132333432317367454b4b5050635332357935'
    #     check.add_position('name 2', 100, 3, total=290, vat=20, nomenclature=nomenclature)

    #     check.add_payment(200)
    #     check.add_payment(300)

    #     expected = {
    #         'external_id': 1,
    #         'user': 'user@host',
    #         'print': False,
    #         'intent': 'sell',
    #         'sno': 0,
    #         'cashier': {
    #             'name': 'Иваров И.П.',
    #             'inn': '1234567890123'
    #         },
    #         'client': {
    #             'name': 'Иванов И.П.',
    #             'inn': '1231231231'
    #         },
    #         'payments': [
    #             {'sum': 100, 'type': 'card'},
    #             {'sum': 200, 'type': 'card'},
    #             {'sum': 300, 'type': 'card'}
    #         ],
    #         'positions': [
    #             {
    #                 'id': 1,
    #                 'name': 'name 0',
    #                 'price': 100,
    #                 'quantity': 1,
    #                 'total': 100,
    #                 'vat': 'no',
    #                 'calculation_method': 'full_payment',
    #                 'calculation_subject': 'product',
    #                 'excise': 19.89,
    #                 'country_code': '643',
    #                 'declaration_number': '10129000/220817/0211234',
    #                 'agent_info': {
    #                     'type': 'commissionaire'
    #                 },
    #                 'supplier_info': {
    #                     'phones': ["+77777777777"],
    #                     'name': "ООО 'Лютик'",
    #                     'inn': "12345678901"
    #                 },
    #                 'nomenclature_code': {
    #                     'code': '019876543210123421sgEKKPPcS25y5'
    #                 }
    #             },
    #             {
    #                 'id': '2',
    #                 'name': 'name 1',
    #                 'price': 100,
    #                 'quantity': 2,
    #                 'total': 200,
    #                 'vat': 'no',
    #                 'measure_name': 'kg',
    #                 'nomenclature_code': {
    #                     'code': '019876543210123421sgEKKPPcS25y5',
    #                     'hex_code': '444D00000096b43f303132333432317367454b4b5050635332357935'
    #                 }
    #             },
    #             {
    #                 'name': 'name 2',
    #                 'price': 100,
    #                 'quantity': 3,
    #                 'total': 290,
    #                 'vat': '20',
    #                 'nomenclature_code': {
    #                     'hex_code': '444D00000096b43f303132333432317367454b4b5050635332357935'
    #                 }
    #             }
    #         ]
    #     }
    #     for key, value in check:
    #         self.assertEqual(expected[key], value)

    #     check.set_print(True)
    #     self.assertTrue(check['print'])
    #     check.set_print(False)
    #     self.assertFalse(check['print'])

    # def test_set_additional_check_props(self):
    #     check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
    #     check.set_additional_check_props('Дополнительный реквизит чека')
    #     self.assertEqual(check['additional_check_props'], 'Дополнительный реквизит чека')

    # def test_set_additional_user_props(self):
    #     check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
    #     check.set_additional_user_props('Наименование', 'Значение')
    #     self.assertEqual(check['additional_user_props'],
    #                      {'name': 'Наименование', 'value': 'Значение'})

    # def test_apply_discount(self):
    #     check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
    #     check.set_client(name='Иванов И.П.', inn='1231231231')
    #     check.set_cashier('Иваров И.П.', '1234567890123')
    #     check.add_position('name 0', price=120.67, oid=1,
    #                        calculation_method=CalculationMethod.FULL_PAYMENT,
    #                        calculation_subject=CalculationSubject.PRODUCT)
    #     check.add_position('name 1', price=113.54, oid=2,
    #                        calculation_method=CalculationMethod.FULL_PAYMENT,
    #                        calculation_subject=CalculationSubject.PRODUCT)
    #     check.apply_discount(50)

    #     self.assertEqual(check['positions'][0]['total'], Decimal('94.91'))
    #     self.assertEqual(check['positions'][1]['total'], Decimal('89.30'))

    # def test_apply_correction_positions(self):
    #     '''
    #     Тест применения алгоритма корректировки позиции
    #     '''

    #     check = Check(1, 'user@host', Intent.SELL, TaxSystem.COMMON)
    #     check.add_position(oid=1, name='Позиция 1', price=Decimal('42.4'),
    #                        quantity=2, total=Decimal(84.5))

    #     check.add_position(oid='2', name="Доставка", price=10)
    #     check.apply_correction_positions()
    #     self.assertEqual(len(check['positions']), 3)
