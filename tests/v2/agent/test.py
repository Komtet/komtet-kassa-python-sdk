# -*- coding: utf-8 -*-
from unittest import TestCase

from komtet_kassa_sdk.v2 import (Agent, AgentType)


class TestAgent(TestCase):
    def setUp(self):
        self.agent = Agent(agent_type=AgentType.AGENT, phone='+79998887766',
                           name='Названиепоставщика', inn='287381373424')

    def test_simple_agent(self):

        expected = {
            'agent_info': {
                'type': 'agent'
            },
            'supplier_info': {
                'phones': ['+79998887766'],
                'name': 'Названиепоставщика',
                'inn': '287381373424'
            }
        }
        self.assertEqual(dict(self.agent), expected)

    def test_paying_agent(self):
        agent_info = Agent(agent_type=AgentType.AGENT, phone='+79998887766',
                           name='Названиепоставщика', inn='287381373424')
        agent_info.set_paying_agent(operation='Операция1', phones=['+79998887766'])

        expected = {
            'agent_info': {
                'type': 'agent',
                'paying_agent': {
                        'operation': 'Операция1',
                        'phones': ['+79998887766']
                }
            },
            'supplier_info': {
                'phones': ['+79998887766'],
                'name': 'Названиепоставщика',
                'inn': '287381373424'
            }
        }
        self.assertEqual(dict(agent_info), expected)

    def test_receive_payments_operator(self):
        agent_info = Agent(agent_type=AgentType.AGENT, phone='+79998887766',
                           name='Названиепоставщика', inn='287381373424')
        agent_info.set_receive_payments_operator(phones=['+79998887766'])

        expected = {
            'agent_info': {
                'type': 'agent',
                'receive_payments_operator': {
                    'phones': ['+79998887766']
                }
            },
            'supplier_info': {
                'phones': ['+79998887766'],
                'name': 'Названиепоставщика',
                'inn': '287381373424'
            }
        }
        self.assertEqual(dict(agent_info), expected)

    def test_money_transfer_operator(self):
        agent_info = Agent(agent_type=AgentType.AGENT, phone='+79998887766',
                           name='Названиепоставщика', inn='287381373424')
        agent_info.set_money_transfer_operator(phones=['+79998887766'], name='Операторперевода',
                                               address='г. Москва, ул. Складочная д.3',
                                               inn='8634330204')

        expected = {
            'agent_info': {
                'type': 'agent',
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
        }
        self.assertEqual(dict(agent_info), expected)
