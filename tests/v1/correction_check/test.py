# -*- coding: utf-8 -*-
from decimal import Decimal
from unittest import TestCase

from komtet_kassa_sdk.v1 import (CorrectionCheck, CorrectionType, Intent, PaymentMethod,
                                 TaxSystem, VatRate)


class TestCorrectionCheck(TestCase):
    def test_check(self):
        check = CorrectionCheck(2, Intent.SELL_CORRECTION, TaxSystem.COMMON)
        check.add_position('name 1', 10, quantity=1)
        check.add_payment(10, PaymentMethod.CARD)
        check.set_correction_data(type=CorrectionType.FORCED, date='2017-09-28', 
                                  description='Отключение электричества', document_number='K11')
        check.set_authorised_person('Иванов И.И.', '123456789012')
        check.set_callback_url('http://test.pro')
        check.set_client(name='Иванов И.П.', inn='1231231231')

        expected = {
            'external_id': 2,
            'intent': 'sellCorrection',
            'sno': 0,
            'print': False,
            'client': {
                'name': 'Иванов И.П.',
                'inn': '1231231231'
            },
            'payments': [
                {'sum': 10, 'type': 'card'},
            ],
            'positions': [
                {
                    'name': 'name 1',
                    'price': 10,
                    'quantity': 1,
                    'total': 10,
                    'vat': 'no'
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


    def test_check_without_document(self):
        check = CorrectionCheck(2, Intent.SELL_CORRECTION, TaxSystem.COMMON)
        check.add_position('name 1', 10, quantity=1)
        check.add_payment(10, PaymentMethod.CARD)
        check.set_correction_data(type=CorrectionType.FORCED, date='2017-09-28', 
                                  description='Отключение электричества')
        check.set_authorised_person('Иванов И.И.', '123456789012')
        check.set_callback_url('http://test.pro')
        check.set_client(name='Иванов И.П.', inn='1231231231')

        expected = {
            'external_id': 2,
            'intent': 'sellCorrection',
            'sno': 0,
            'print': False,
            'client': {
                'name': 'Иванов И.П.',
                'inn': '1231231231'
            },
            'payments': [
                {'sum': 10, 'type': 'card'},
            ],
            'positions': [
                {
                    'name': 'name 1',
                    'price': 10,
                    'quantity': 1,
                    'total': 10,
                    'vat': 'no'
                }
            ],
            'correction': {
                'type': 'forced',
                'date': '2017-09-28',
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
