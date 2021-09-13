# -*- coding: utf-8 -*-
from unittest import TestCase

from komtet_kassa_sdk.v2 import (CorrectionCheck, CorrectionType, Intent, MesureTypes,
                                 PaymentMethod, PaymentObject, Position, TaxSystem, VatRate)


class TestCorrectionCheck(TestCase):
    def test_check(self):
        check = CorrectionCheck(2, Intent.SELL_CORRECTION)
        check.set_company(payment_address='ул. им Дедушки на деревне д.5',
                          tax_system=TaxSystem.COMMON)
        check.set_client(email='client@client.ru', phone='+79992410085',
                         name='Иванов Иван', inn='516974792202')
        check.set_payment(50)
        check.set_correction_info(CorrectionType.INSTRUCTION, '2017-09-28', 'K11',
                                  'Отключение электричества')
        position = Position(name='Товар', price=10, quantity=5, total=50,
                            measure=MesureTypes.PIECE, payment_method=PaymentMethod.FULL_PAYMENT,
                            payment_object=PaymentObject.PRODUCT, vat=VatRate.RATE_NO)
        check.add_position(position)
        check.set_cashier(name='Кассир', inn='8634330201')
        check.set_additional_check_props('445334544')
        check.set_authorised_person('Иванов И.И.', '123456789012')
        check.set_callback_url('http://test.pro')

        expected = {
            'external_id': 2,
            'intent': 'sellCorrection',
            'correction_info': {
                'type': 'instruction',
                'base_date': '2017-09-28',
                'base_number': 'K11',
                'base_name': 'Отключение электричества'
            },
            'company': {
                'payment_address': 'ул. им Дедушки на деревне д.5',
                'sno': 0
            },
            'client': {
                'email': 'client@client.ru',
                'phone': '+79992410085',
                'name': 'Иванов Иван',
                'inn': '516974792202'
            },
            'positions': [{
                'name': 'Товар',
                'price': 10,
                'quantity': 5,
                'total': 50,
                'measure': 0,
                'payment_method': 'full_payment',
                'payment_object': 'product',
                'vat': 'no'
            }],
            'cashier': {
                'name': 'Кассир',
                'inn': '8634330201'
            },
            'additional_check_props': '445334544',
            'authorised_person': {
                'name': 'Иванов И.И.',
                'inn': '123456789012'
            },
            'payments': [{'type': 'card', 'sum': 50}],
            'callback_url': 'http://test.pro'
        }

        for key, value in check:
            self.assertEqual(expected[key], value)

    def test_additional_user_props(self):
        '''
        Тест дополнительных параметров чека
        '''
        check = CorrectionCheck(2, Intent.SELL_CORRECTION)
        check.set_additional_user_props('получатель', 'Васильев')

        self.assertEqual(check['additional_user_props']['name'], 'получатель')
        self.assertEqual(check['additional_user_props']['value'], 'Васильев')


class TestSetCashier(TestCase):

    def test_set_cashier_with_inn_in_correction_check(self):
        check = CorrectionCheck(2, Intent.SELL_CORRECTION)
        check.set_authorised_person('Иваров И.П.', '1234567890123')
        self.assertDictEqual(check['authorised_person'], {
            'name': 'Иваров И.П.',
            'inn': '1234567890123'
        })

    def test_set_cashier_without_inn_in_correction_check(self):
        check = CorrectionCheck(2, Intent.SELL_CORRECTION)
        check.set_authorised_person('Иваров И.П.')
        self.assertDictEqual(check['authorised_person'], {
            'name': 'Иваров И.П.'
        })
