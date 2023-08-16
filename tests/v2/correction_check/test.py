# -*- coding: utf-8 -*-
from unittest import TestCase

from komtet_kassa_sdk.v2 import (CorrectionCheck, CorrectionType, Intent, MeasureTypes,
                                 PaymentMethod, PaymentObject, Position, TaxSystem, VatRate)


class TestCorrectionCheck(TestCase):
    def test_check(self):
        check = CorrectionCheck(2, Intent.SELL_CORRECTION)
        check.set_company(payment_address='ул. им Дедушки на деревне д.5',
                          tax_system=TaxSystem.COMMON)
        check.set_client(email='client@client.ru', phone='+79992410085',
                         name='Иванов Иван', inn='516974792202')
        check.add_payment(50)
        check.set_correction_info(CorrectionType.INSTRUCTION, '2017-09-28', 'K11')
        position = Position(name='Товар', price=10, quantity=5, total=50,
                            measure=MeasureTypes.PIECE, payment_method=PaymentMethod.FULL_PAYMENT,
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
                'base_number': 'K11'
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

        check.set_print(True)
        self.assertTrue(check['print'])
        check.set_print(False)
        self.assertFalse(check['print'])

    def test_correction_info(self):
        '''
        Тест информации о коррекции
        '''
        check = CorrectionCheck(3, Intent.SELL_CORRECTION)
        check.set_correction_info(CorrectionType.SELF, '2017-09-28', 'K11')

        self.assertEqual(check['correction_info']['type'], 'self')
        self.assertEqual(check['correction_info']['base_date'], '2017-09-28')
        self.assertEqual(check['correction_info']['base_number'], 'K11')

    def test_correction_info_without_base_number(self):
        '''
        Тест информации о коррекции без номера документа основания для коррекции
        '''
        check = CorrectionCheck(3, Intent.SELL_CORRECTION)
        check.set_correction_info(CorrectionType.INSTRUCTION, '2022-09-28')

        self.assertEqual(check['correction_info']['type'], 'instruction')
        self.assertEqual(check['correction_info']['base_date'], '2022-09-28')


    def test_additional_user_props(self):
        '''
        Тест дополнительных параметров чека
        '''
        check = CorrectionCheck(2, Intent.SELL_CORRECTION)
        check.set_additional_user_props('получатель', 'Васильев')

        self.assertEqual(check['additional_user_props']['name'], 'получатель')
        self.assertEqual(check['additional_user_props']['value'], 'Васильев')

    def test_client_in_check(self):
        check = CorrectionCheck(oid=2, intent=Intent.SELL)
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

    def test_sectoral_check_props(self):
        '''
        Тест данных об отраслевой принадлежности чека
        '''
        check = CorrectionCheck(oid=2043, intent=Intent.SELL)
        check.add_sectoral_check_props('001', '01.01.2001', '170/21',
                                       'Ид1=Знач1&Ид2=Знач2&Ид3=Знач3')

        self.assertEqual(check['sectoral_check_props'][0]['federal_id'], '001')
        self.assertEqual(check['sectoral_check_props'][0]['date'], '01.01.2001')
        self.assertEqual(check['sectoral_check_props'][0]['number'], '170/21')
        self.assertEqual(check['sectoral_check_props'][0]['value'], 'Ид1=Знач1&Ид2=Знач2&Ид3=Знач3')

    def test_operating_check_props(self):
        '''
        Тест данных об отраслевой принадлежности чека
        '''
        check = CorrectionCheck(oid=2043, intent=Intent.SELL)
        check.set_operating_check_props('0', 'Данные операции', '03.11.2020 12:05:31')

        self.assertEqual(check['operating_check_props']['name'], '0')
        self.assertEqual(check['operating_check_props']['value'], 'Данные операции')
        self.assertEqual(check['operating_check_props']['timestamp'], '03.11.2020 12:05:31')


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
