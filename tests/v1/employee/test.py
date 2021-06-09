# -*- coding: utf-8 -*-
from unittest import TestCase

from komtet_kassa_sdk.v1 import (Client, Employee, EmployeeInfo, EmployeeType)
from mock import patch
from ...helpers.mock import (ResponseMock,)


class TestEmployee(TestCase):
    def setUp(self):
        self.client = Client('shop-id', 'secret-key')
        self.response_mock = ResponseMock(
            id=1, name='Ivanov Ivan Ivanovich', login='test_login',
            password='test_password', pos_id='POS_KEY')

    def test_create_order_success(self):
        with patch('komtet_kassa_sdk.v1.client.requests') as requests:
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
        with patch('komtet_kassa_sdk.v1.client.requests') as requests:
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
        with patch('komtet_kassa_sdk.v1.client.requests') as requests:
            requests.delete.return_value = ResponseMock()

            result = self.client.delete_employee(1)
            self.assertEqual(result, True)
