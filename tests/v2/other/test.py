# -*- coding: utf-8 -*-
from decimal import Decimal
from unittest import TestCase

from komtet_kassa_sdk.v2 import (Check, Client, Intent, MesureTypes,
                                 PaymentMethod, Position, PaymentObject, TaskInfo, TaxSystem, VatRate)
from komtet_kassa_sdk.v2.lib.helpers import correction_positions
from mock import patch
from ...helpers.mock import ResponseListMock


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


class TestMultiTasks(TestCase):
    def setUp(self):
        self.client = Client('shop-id', 'secret-key')
        self.response_mock = ResponseListMock({
            idx: dict(id=idx, external_id=idx, print_queue_id=3, state='new') for idx in range(5)
        })

    def test_create_multi_tasks_success(self):
        with patch('komtet_kassa_sdk.v2.client.requests') as requests:
            requests.post.return_value = self.response_mock
            checks = []
            for i in range(5):
                check = Check(oid=2043, intent=Intent.SELL)
                position = Position(id=1, name='Товар', price=100, quantity=1,
                                    measure=MesureTypes.PIECE, vat=VatRate.RATE_NO,
                                    payment_method=PaymentMethod.FULL_PAYMENT,
                                    payment_object=PaymentObject.PRODUCT)
                check.add_position(position)
                check.add_payment(100)
                position = Position(id=1, name='Товар', price=100, quantity=2,
                                    measure=MesureTypes.KILOGRAMM, vat=VatRate.RATE_NO,
                                    payment_method=PaymentMethod.FULL_PAYMENT,
                                    payment_object=PaymentObject.PRODUCT)
                check.add_position(position)
                check.add_payment(200)
                position = Position(id=1, name='Товар', price=300, quantity=3, total=290,
                                    measure=MesureTypes.PIECE, vat=VatRate.RATE_20,
                                    payment_method=PaymentMethod.FULL_PAYMENT,
                                    payment_object=PaymentObject.PRODUCT)
                check.add_position(position)
                check.add_payment(300)

                checks.append(check)

            checks_info = self.client.create_tasks(checks, 2)
            self.assertIsInstance(checks_info, list)

            for idx, check_info in enumerate(checks_info):
                self.assertIsInstance(check_info, TaskInfo)
                expected = dict(id=idx, external_id=idx, print_queue_id=3, state='new')
                for key, value in expected.items():
                    self.assertEqual(value, getattr(check_info, key))


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
